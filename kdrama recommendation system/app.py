import os
import pickle
import pandas as pd
import streamlit as st
import numpy as np
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
import requests
from PIL import Image

def fetch_poster(kdrama_name):
    kdrama_name = kdrama_name.split("(")[0].strip()
    kdrama_name_encoded = requests.utils.quote(kdrama_name)
    search_url = f'https://api.themoviedb.org/3/search/tv?api_key=2b46af959e206444738045dc5ebd0d94&query={kdrama_name_encoded}'
    
    # Make the request to TMDb API
    response = requests.get(search_url)
    json_data = response.json().get('results')
    
    if not json_data:
        return None  # Return None if no results found
    
    kdrama_id = None
    for result in json_data:
        if result.get('original_language') == 'ko':
            kdrama_id = result.get('id')
            break
    
    if kdrama_id is None:
        return None  # Return None if no Korean drama found
    
    url = f'https://api.themoviedb.org/3/tv/{kdrama_id}?api_key=2b46af959e206444738045dc5ebd0d94'
    response = requests.get(url)
    new_data = response.json()
    poster_path = new_data.get("poster_path")

    if poster_path is None:
        return None  # Return None if poster_path is not available

    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"

    return full_path


    
current_directory = os.path.abspath(os.getcwd())
kfile_path = os.path.join(current_directory, 'kdramas.pkl')
kdramas = pd.read_pickle(kfile_path)
sfile_path = os.path.join(current_directory, 'similarities.pkl')
similarities = pd.read_pickle(sfile_path)


kdramalist = kdramas["Title"].values
st.header("2024 KDrama Recommendation System")

import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")


imageUrls = [
    fetch_poster('Crash Landing on You (2019)'),
    fetch_poster('Alchemy of Souls (2022)'),
    fetch_poster('Business Proposal (2022)'),
    fetch_poster('Twenty-Five Twenty-One (2022)'),
    fetch_poster("It's Okay to Not Be Okay (2022)"),
    fetch_poster('The Glory (2023)'),
    ]


imageCarouselComponent(imageUrls=imageUrls, height=200)
selected_kdrama = st.selectbox("Select kdrama from dropdown", kdramalist)



def recommend(kdrama):
    # Assuming user_ratings is a dictionary containing user ratings for kdramas
    # If a user hasn't rated a kdrama, the rating is considered as 0
    kdramas_csv = pd.read_csv('top100kdramasin2024.csv')
    score = kdramas_csv['Score']
    score_list = []
    for i in score:
        m = i.index('(')
        i = i[0:m]
        score_list.append(i)


    user_ratings = score_list 

    index = kdramas[kdramas['Title'] == kdrama].index[0]

    # Assuming 'Genres', 'Tags', 'Main Role' are categorical columns
    categorical_columns = ['Genres', 'Tags', 'Main Role']

    def safe_preprocess(doc):
        try:
            if isinstance(doc, np.ndarray):
                return [' '.join([str(item) for item in row]) for row in doc]
            else:
                return str(doc)
        except AttributeError:
            return str(doc)

    def custom_tokenizer(doc):
        try:
            # If the input is already a string or bytes-like object, return it as is
            if isinstance(doc, (str, bytes)):
                return doc
            # If the input is a list of elements, join them into a single string
            elif isinstance(doc, list):
                return ' '.join([str(item) for item in doc])
        except TypeError:
            pass  # Handle other types gracefully
        return str(doc)

    # Use CountVectorizer to convert categorical columns to numerical format
    cv = CountVectorizer(max_features=100, tokenizer=custom_tokenizer, preprocessor=safe_preprocess)
    vals = kdramas_csv[categorical_columns].values
    vals = np.array([custom_tokenizer(row) for row in vals], dtype='U')  # Apply custom_tokenizer to each row
    vector = cv.fit_transform(vals).toarray()

    # Create a DataFrame with the vectorized features
    vectorized_df = pd.DataFrame(vector, columns=cv.get_feature_names_out(categorical_columns))

    # Concatenate the vectorized features with the original dataframe
    kdramas_csv_vectorized = pd.concat([kdramas_csv, vectorized_df], axis=1)

    # Now, you can use the vectorized features for cosine similarity
    content_similarity = cosine_similarity(kdramas_csv_vectorized.iloc[:, -vectorized_df.shape[1]:], kdramas_csv_vectorized.iloc[:, -vectorized_df.shape[1]:])
    
    # Assuming user_ratings is a pandas Series
    user_ratings = np.array(user_ratings)

    # Collaborative filtering similarity based on user ratings
    collaborative_similarity = cosine_similarity(user_ratings.reshape(1,-1), user_ratings.reshape(1,-1))

    # Combine content-based and collaborative filtering similarities with weights
    alpha = 0.7  # Weight for content-based similarity
    beta = 0.3  # Weight for collaborative filtering similarity
    combined_similarity = alpha * content_similarity + beta * collaborative_similarity

    distance = sorted(list(enumerate(combined_similarity[index])), reverse=True, key=lambda vector: vector[1])

    recommend_kdrama = []
    recommend_poster = []

        # Create a dictionary to store unique values
    unique_values_dict = {}

    # Iterate through the list of tuples
    for key, value in distance:
        # Check if the value is already in the dictionary
        if value not in unique_values_dict:
            # If not, add the key-value pair to the dictionary
            unique_values_dict[value] = key


    distance_list = []
    for key, value in unique_values_dict.items():
        tuple = (value, key)
        distance_list.append(tuple)
    

    for i in distance_list[1:6]:  
        kdrama_id = kdramas_csv.iloc[i[0]].ID
        kdrama_name = kdramas_csv.iloc[i[0]].Title
        recommend_kdrama.append(kdrama_name)
        poster_url = fetch_poster(kdrama_name)
        recommend_poster.append(poster_url)
    
    return recommend_kdrama, recommend_poster

if st.button("Show Recommendations"):
    # Add your recommendation logic here based on the selected_kdrama
    kdrama_name, kdrama_poster = recommend(selected_kdrama)
    col1, col2, col3, col4, col5  = st.columns(5)

    with col1:
        st.text(kdrama_name[0])
        st.image(kdrama_poster[0])
    with col2:
        st.text(kdrama_name[1])
        st.image(kdrama_poster[1])
    with col3:
        st.text(kdrama_name[2])
        print(kdrama_poster[2])
        st.image(kdrama_poster[2])
    with col4:
        st.text(kdrama_name[3])
        st.image(kdrama_poster[3])
    with col5:
        st.text(kdrama_name[4])
        
        st.image(kdrama_poster[4])



