from twitter_redistwo import TwitterAPITwo
from twitter_objects import Follows, Tweet
import time
import pandas as pd

def main():
    api = TwitterAPITwo(host="localhost", port=6379, db=0, decode_responses=True)

    # Set the time duration for counting (e.g., 1 second)
    duration = 1

    # Example usage:
    tweet = pd.read_csv('tweet.csv')

    # Get the current time
    start_time = time.time()

    # Initialize a counter for function calls
    call_count = 0

    for index, row in tweet.iterrows():
        user_id = row['USER_ID']
        tweet_text = row['TWEET_TEXT']

        # Make API calls
        api.postTweet(user_id, tweet_text)
        api.updateHomeTimeline(user_id)

        call_count += 1
        print("Retrieved " + str(call_count) + " Home Timeline(s)")


        # Check if the duration has been reached
        if time.time() - start_time >= duration:
            break

if __name__ == '__main__':
    main()