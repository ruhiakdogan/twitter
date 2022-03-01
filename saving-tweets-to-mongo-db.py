% % time
import tweepy
import configparser
import pandas as pd
import schedule
import time
import pymongo

api_key = ""
api_key_secret = ""

access_token = ""
access_token_secret = ""
beerer_token = ""
m_client = pymongo.MongoClient("")

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
client = tweepy.Client(bearer_token=beerer_token)
api = tweepy.API(auth, wait_on_rate_limit=True)

db = m_client.some_database
tarkan = db.tarkan

limit = 100


def get_tweets():
    tweets = tweepy.Cursor(api.search_tweets, q=["ve"], count=100, tweet_mode="extended", lang='tr').items(limit)

    for tweet in tweets:
        print("selamlar")
        if (tarkan.count_documents({"tweet": tweet.full_text}) == 0):
            print("merhaba")
            if (tweet.full_text.startswith("RT @") == False):
                tarkan.insert_one({"tweet": tweet.full_text})
            else:
                text = ' '.join(tweet.full_text.split()[2:])
                tarkan.insert_one({"tweet": text})


schedule.every(3.5).seconds.do(get_tweets)

while True:
    schedule.run_pending()
    time.sleep(1)