# -*- coding: utf-8 -*-

import argparse
import sys
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
import sqlite3
from local_config import *
#from implementation import *
import itertools
import subprocess
import pickle
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
import re


########################################

parser = argparse.ArgumentParser(description='Look for the data with the Twitter API')

search_word = sys.argv[1]

########################################

db = "twit_data.db"
conn = sqlite3.connect(db)
c = conn.cursor()

########################################

f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

########################################
non_words =[]
#non_words = list(punctuation)
non_words.extend(['¿', '¡', ':'])
non_words.extend(map(str,range(10)))

snowball_stemmer = SnowballStemmer('spanish')

def create_word_features(words):

    useful_words = [ snowball_stemmer.stem(word.lower()) for word in words if word not in non_words]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict


########################################

def cleaning_tweets(tweet):

    tweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet)
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)
    tweet = re.sub(r'#\w+ ?', '', tweet)
    tweet = re.sub(r'_\w+ ?', '', tweet)
    tweet = re.sub(r'\([^)]*\)', '', tweet)
    tweet = re.sub(r'!', '', tweet)
    tweet = re.sub(r'www\.\S+\.com', '', tweet)


    return tweet

########################################
class twitter_listener(StreamListener):

    def __init__(self, num_tweets_max):

        self.counter = 0
        self.num_tweets_max = num_tweets_max

    def on_data(self, data):

        try:
            decoded = json.loads(data)
            self.counter += 1
            if self.counter >= self.num_tweets_max:
                return False


        except Exception as e:
            print (e)
            return True




        user = '@' + decoded.get('user').get('screen_name')
        created = decoded.get('created_at')
        content = decoded['text']
        tweet_id = decoded['id']

        tweet = '%s|%s|%s|%s|\n\n' % (tweet_id, user,created,content)


        if ((decoded.get('user').get('friends_count') < 10) or
            (decoded.get('user').get('friends_count') >= 1000) or
            (decoded.get('user').get('followers_count') < 15) or
            (content.startswith('RT ') or
            (decoded.get('user').get('statuses_count') > 100000))):

            pass

        else:

            content_prev = content
            content = cleaning_tweets(content)
            words = word_tokenize(content)

            #### Remove duplicates characters #########
            content_pos = []
            for word in words:
                content_pos.append(''.join(ch for ch, _ in itertools.groupby(word)))

            words = create_word_features(content_pos)
            polarity = classifier.classify(words)


            c.execute('INSERT INTO BaseTweets(tweet_id, User, Created_at, content, Polarity) VALUES(?,?,?,?,?)', (tweet_id, user, created, content_prev, polarity))
            conn.commit()
            print(tweet)


        return True

    def on_error(self, status):

        print(status)


if __name__ == "__main__":

    if sys.argv[1] == None:

        print('Please, insert again the product you want to get tweets of')
        pass

    else:

        print('starting')

        auth = tweepy.OAuthHandler(cons_tok, cons_sec)
        auth.set_access_token(app_tok, app_sec)

        twitter_stream = Stream(auth, twitter_listener(50))
        twitter_stream.filter(track = [search_word] , languages = ['es'])

        try:
            conn = sqlite3.connect(db)

        except Exception as e:
            print(e.__doc__)

        finally:
            conn.close()
            subprocess.call(['sqlite_web', 'twit_data.db'])




