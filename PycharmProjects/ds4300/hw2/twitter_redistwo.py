from twittermainutils import TwitterDBUtils
import redis
import pandas as pd
import random
from datetime import datetime
import time

# Strategy Two

class TwitterAPITwo:

    def __init__(self, host, port, db, decode_responses):
        self.r = redis.Redis(host=host, port=port,db=db, decode_responses=decode_responses)

    def postTweet(self, user_id, tweet_text):
        start_time = time.time()

        # Increment a counter for unique tweet_id
        tweet_id = self.r.incr('tweet_id_counter')

        tweet_key = f'Tweet {tweet_id}:'
        tweet_value = f'User {user_id}: {tweet_text} {datetime.now().time().strftime("%H:%M:%S")}'

        # Use pipeline for more efficient Redis operations
        with self.r.pipeline() as pipe:
            pipe.set(tweet_key, tweet_value)
            pipe.lpush(f'HomeTimeline:{user_id}', tweet_key)
            pipe.execute()

        print(f'Tweet {tweet_id} posted for User {user_id}')

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total time taken to post tweet: {total_time} seconds")

    def updateHomeTimeline(self, user_id):
        start_time = time.time()

        # Get the tweets from the user's home timeline
        home_timeline_key = f'HomeTimeline:{user_id}'
        home_timeline_tweets = self.r.lrange(home_timeline_key, 0, -1)

        user_idlist = []
        time_list = []

        for tweet_key in home_timeline_tweets:
            tweet_value = self.r.get(tweet_key)
            user_id = tweet_value.split(':')[0].split(' ')[-1]
            timestamp = tweet_value.split()[-2:]
            timestamp = ":".join(timestamp)
            user_idlist.append(user_id)
            time_list.append(timestamp)

        # Create a DataFrame
        home_timeline_df = pd.DataFrame({'USER_ID': user_idlist, 'TWEET_TS': time_list})

        # Sort by timestamp
        sorted_home_timeline = home_timeline_df.sort_values(by='TWEET_TS', ascending=False)

        # Get the row with the most current timestamp
        result_row = sorted_home_timeline.head(10)
        print(result_row)

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total time taken to fetch home timeline: {total_time} seconds")
