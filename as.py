import tweepy
import json
import os
from dotenv import load_dotenv
load_dotenv()

consumer_key = os.getenv('api_key')
consumer_secret = os.getenv('api_key_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = tweepy.API(self.auth)


class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token( access_token, access_token_secret )
        return auth


class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    def stream_tweets(self,fetched_tweets_filename,lists):

        streamListener = StreamListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = tweepy.Stream(auth ,listener=streamListener,tweet_mode='extended')
        stream.filter(track=lists)


class StreamListener(tweepy.StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            dicts = json.loads(data)
            print(dicts)
            self.on_status(dicts)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("error on_data: %s" % str(e))
        return True         
    def on_status(self, tweet):
        self.aut = TwitterAuthenticator().authenticate_twitter_app()
        api=tweepy.API(self.aut)
        recipient_id = tweet['user']['id']
        api.send_direct_message(recipient_id,api.get_status(tweet['in_reply_to_status_id']).text) 
        return True   
    def on_error(self, status):
        if status == 420:
            return False
        print(status)


if __name__ == "__main__":      
    lists = ["@tweetaholic"]
    fetched_tweets_filename = "tweets.json" 
    twitter_stream = TwitterStreamer()
    twitter_stream.stream_tweets(fetched_tweets_filename,lists)
     