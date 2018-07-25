from livescraper.query import MyStreamListener, query_tweets

from libs.filename_utils import get_locations
from libs.reading_utils import get_twitter

from tweepy import OAuthHandler, Stream
import pandas as pd

import time

import logging

class TestMyStreamListener():
    def setup_method(self):
        self.keywords = {'bitcoin': ['bitcoin', 'BTC'], 'dashcoin': ['dashcoin', 'DASH', 'darkcoin'], 'dogecoin': ['dogecoin', 'DOGE'], 'ethereum': ['ethereum', 'ETH'], 'litecoin': ['litecoin', 'LTC'], 'ripple': ['ripple', 'XRP'], 'monero': ['monero', 'XMR'], 'stellar': ['stellar', 'STR']}
        self.keywordsOnly = [value for key, values in self.keywords.items() for value in values]
        
        self.logger = logging.getLogger()

        _, self.currRoot_dir = get_locations()
        self.logger.basicConfig = logging.basicConfig(filename= self.currRoot_dir + '/logs/tests/live.txt', level=logging.INFO)
        self.listener = MyStreamListener(self.keywords, self.logger, tweetCount=10)

        consumer_key, consumer_secret, access_token, access_token_secret = get_twitter()

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.myStream = Stream(auth=auth, listener=self.listener)

        self.myStream.filter(track=self.keywordsOnly, languages=['en'])
        self.df, self.userData, _ = self.listener.get_data()
        
    def test_on_status(self):
        assert(self.df.shape[1] >= 9)
        assert(self.userData.shape[1] >= 9)

        assert(sum(self.df['ID'].astype(str).str.len()) >= 19 * self.df.shape[1])
        assert('Tweet' in self.df)
        assert(sum(self.df['Time'].astype(str).str.len()) >= 10 * self.df.shape[1])
        assert(sum(self.df['User'].str.count(' ')) == 0)
        assert(sum(self.df['Likes']) >= 0)
        assert(sum(self.df['Replies']) >= 0)
        assert(sum(self.df['Retweets']) >= 0)
        assert('in_response_to' in self.df)

        assert(sum(self.df['response_type'].isin(['tweet', 'retweet', 'quoted_status', 'quoted_retweet', 'reply'])) == self.df.shape[1])
        assert(sum(self.df['coinname'].isin(self.keywordsOnly)) == self.df.shape[1])
    

class Testquery_tweets():
    def setup_method(self):
        self.keywords = {'bitcoin': ['bitcoin', 'BTC'], 'dashcoin': ['dashcoin', 'DASH', 'darkcoin'], 'dogecoin': ['dogecoin', 'DOGE'], 'ethereum': ['ethereum', 'ETH'], 'litecoin': ['litecoin', 'LTC'], 'ripple': ['ripple', 'XRP'], 'monero': ['monero', 'XMR'], 'stellar': ['stellar', 'STR']}
        self.keywordsOnly = [value for key, values in self.keywords.items() for value in values]
        
        self.logger = logging.getLogger()

        _, self.currRoot_dir = get_locations()
        self.logger.basicConfig = logging.basicConfig(filename= self.currRoot_dir + '/logs/tests/live.txt', level=logging.INFO)
        self.qt = query_tweets(self.keywords, tweetCount=10)

    def test_get_stream(self):
        listener = self.qt.perform_search()
        df, userData, _ = listener.get_data()

        assert(df.shape[1] >= 9)
        assert(userData.shape[1] >= 9)

        assert(sum(df['ID'].astype(str).str.len()) >= 19 * df.shape[1])
        assert('Tweet' in df)
        assert(sum(df['Time'].astype(str).str.len()) >= 10 * df.shape[1])
        assert(sum(df['User'].str.count(' ')) == 0)
        assert(sum(df['Likes']) >= 0)
        assert(sum(df['Replies']) >= 0)
        assert(sum(df['Retweets']) >= 0)
        assert('in_response_to' in df)

        assert(sum(df['response_type'].isin(['tweet', 'retweet', 'quoted_status', 'quoted_retweet', 'reply'])) == df.shape[1])
        assert(sum(df['coinname'].isin(self.keywordsOnly)) == df.shape[1])


    def test_save_data(self):
        pass
    