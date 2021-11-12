import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

consumer_key = os.getenv("twitter_consumer_key")
consumer_secret = os.getenv("twitter_consumer_secret")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)
for tweet in tweepy.Cursor(api.search_tweets, q=['ratio',"ratio'd"]).items(10):
    print(tweet.text)
