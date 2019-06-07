import sys
sys.path.insert(0, '../src')
from utils import *
import pickle

'''
   save 10000 first tweets to misc/tweets_10000
'''

tweet_list = get_tweets(N=10000)
f = open("misc/tweets_10000", "wb")
pickle.dump(tweet_list,f)
f.close()

