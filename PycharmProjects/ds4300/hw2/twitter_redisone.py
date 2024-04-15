"""
Created on Thu Feb  4 21:56:24 2021

@author: rachlin
@file  : redis_test.py
"""


#Strategy 1
from twittermainutils import TwitterDBUtils
import redis
import pandas as pd
import random
from datetime import datetime
import time

class TwitterAPI:


    def __init__(self, host, port, db, decode_responses):
        self.r = redis.Redis(host=host, port=port,db=db, decode_responses=decode_responses)

    def getTweet(self):
        N = 1000000
        tweets = pd.read_csv('tweet.csv')
        start = time.time()
        for index, row in tweets.iterrows():
            user_id = row['USER_ID']
            tweet_text = row['TWEET_TEXT']
            tweet_ts = datetime.now().time()
            # Format the time as a string
            tweet_ts= tweet_ts.strftime("%H:%M:%S")
            tweet_id = index
            tweet = f'Tweet {tweet_id}:'
            self.r.set(tweet, f'User {user_id}: {tweet_text} {tweet_ts}')
            print(tweet)
        finish = time.time()
        diff = finish - start
        rate = N / diff
        print(f'Stored {N} keys in {diff} seconds (Rate={rate}/sec')



    def getTimeline(self):
        start_time = time.time()

        # Assuming r is your Redis connection object
        tweets_keys = self.r.keys('*')

        # Assuming you want to get the values associated with the keys
        tweets_values = [key for key in tweets_keys]

        user_idlist = []
        time_list = []

        for vals in tweets_values:
            user_id = vals.split(':')
            user_id = user_id[0].split(' ')[-1]
            timestamp = vals[-3:]
            timestamp = ":".join(timestamp)
            user_idlist.append(user_id)
            time_list.append(timestamp)


        # Create a DataFrame
        tweets_df = pd.DataFrame({'USER_ID': user_idlist, 'TWEET_TS': time_list})

        follows_sample = pd.read_csv('follows.csv')
        follows_list = follows_sample['USER_ID'].astype(str).tolist()


        user_idlist = [value for value in user_idlist if value in follows_list]

        if not user_idlist:
            print("No matching users found in follows.csv")
            return

        random_user = random.choice(user_idlist)

        print("Generating tweets for " + str(random_user))

        user_data = tweets_df[tweets_df['USER_ID'].isin(user_idlist)]

        sorted_user_data = user_data.sort_values(by='TWEET_TS', ascending=False)

        # Get the row with the most current timestamp
        result_row = sorted_user_data.head(10)
        print(result_row)

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total time taken: {total_time} seconds")



