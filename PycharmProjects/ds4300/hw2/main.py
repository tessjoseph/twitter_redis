
from twitter_redistwo import TwitterAPITwo
from twitter_redisone import TwitterAPI
from twitter_objects import Follows, Tweet

import time
import pandas as pd

def main():
    # Authenticate
    api = TwitterAPI(host="localhost", port=6379, db=0, decode_responses=True)
    call_count = 0
    api.getTweet()

    # Set the time duration for counting (e.g., 1 second)
    duration = 1

    # Get the current time
    start_time = time.time()
    while start_time:
        api.getTimeline()
        call_count += 1
        print("Retrieved " + str(call_count) + " Home Timeline(s)")

        # Check if the duration has been reached
        if time.time() - start_time >= duration:
            break



if __name__ == '__main__':
    main()