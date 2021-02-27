# -*- coding: utf-8 -*-

import json
import tweepy
import re

from utils.s3_writer_operator import HandlerS3Writer

class Tweext:

    def __init__(self):
        # Get credentials
        try:
            # Open credentials file and load it into an json object
            f = open('credentials.json')
            credentials = json.load(f)

            # Define credentials variables
            self.consumer_key = credentials['consumer_key']
            self.consumer_secret_key = credentials['consumer_secret_key']
            self.access_token = credentials['access_token']
            self.secret_access_token = credentials['secret_access_token']
        except IOError:
            print('There is a problem with your credentials file, please check the docs.')
        finally:
            f.close()

    def authenticate(self):
        # Connect to Twitter API
        print('==================== Tweext ====================')
        print('Welcome to Tweext v. 0.0.1')
        print('Authenticating...')

        auth = tweepy.OAuthHandler(
            consumer_key = self.consumer_key,
            consumer_secret = self.consumer_secret_key
        )
        
        auth.set_access_token(
            key = self.access_token,
            secret = self.secret_access_token
        )

        self.api = tweepy.API(auth)

        # Get authenticated user information
        me = self.api.me()
        my_id = me.id_str
        my_name = me.name
        my_screen_name = me.screen_name

        print('Authenticated user information:')
        print('ID: ' + my_id + ' | Name: ' + my_name + ' | Screen Name: @' + my_screen_name)
        print('Ready for get data...')

    def start_extraction(self, keyword, limit=1000):
        # Using Cursor + Search to get tweets | excluding replies and retweets
        print('Looking for recent tweets containing "' + keyword + '"')
        tweets = tweepy.Cursor(
            self.api.search,
            q = keyword + ' exclude:retweets exclude:replies',
            lang = 'pt',
            tweet_mode = 'extended',
            result_type = 'recent'
        ).items(limit)

        # Create the headers
        buffer = ''
        headers = 'tweet_data,tweet_text,tweet_favs,tweet_author,tweet_author_verified'
        buffer += headers

        # Add tweets to buffer
        for tweet in tweets:
            # Extract tweet information
            tweet_data = str(tweet.created_at).replace(' ', 'T')
            tweet_text = '"' + tweet.full_text.replace('\n', '').replace('"', '\'') + '"'
            tweet_favs = str(tweet.favorite_count)
            tweet_author = tweet.user.screen_name
            tweet_author_verified = str(tweet.user.verified)

            # Creating the line
            line = '\n' + tweet_data + ',' + tweet_text + ',' + tweet_favs + ',' + tweet_author + ',' + tweet_author_verified
            buffer += line
        
        HandlerS3Writer(
            extracted_file = buffer,
            extraction_name = 'tweets.csv',
            extraction_source = 'twitter'
        )

        print('Process done.')