import tweepy
import os
from dotenv import load_dotenv
import random

load_dotenv()

consumer_key = os.getenv("twitter_consumer_key")
consumer_secret = os.getenv("twitter_consumer_secret")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)


def find_ratio():
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, result_type='popular', q=["ratio", "ratio'd"], lang="en").items(10):
        tweets.append(tweet)
    one_tweet = random.choice(tweets)
    return one_tweet.id

