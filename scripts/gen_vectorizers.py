import sys
sys.path.insert(0, '../src')
from utils import *
import pickle

'''
    save various CountVectorizers, along with their associated word frequencies
'''

tweet_list = get_tweets(N=1000)
tweet_list_nopunct = get_tweets(N=1000, b_punctuation=False)

fr_stopwords = french_stopwords()

''' punctuation - no preprocessing '''
[v1, X1] = build_vectorizer(tweet_list)

f_v1 = open("vectorizers/vect1", "wb")
f_X1 = open("X/X1", "wb")
pickle.dump(v1,f_v1)
pickle.dump(X1,f_X1)
f_v1.close()
f_X1.close()

''' no punctuation - no preprocessing '''
[v2, X2] = build_vectorizer(tweet_list_nopunct)

f_v2 = open("vectorizers/vect2", "wb")
f_X2 = open("X/X2", "wb")
pickle.dump(v2,f_v2)
pickle.dump(X2,f_X2)
f_v2.close()
f_X2.close()

#''' punctuation/no stopwords/stemming/no accent'''
#[vectorizer1, X1] = build_vectorizer(tweet_list, stopwords=fr_stopwords, b_stemming=True, b_rmaccent=True)
#
#f1 = open("vocs/voc1", "wb")
#pickle.dump(vectorizer1, f1)
#f1.close()

#''' no punctuation/no stopwords/stemming/no accent'''
#[vectorizer2, words_freq2] = build_vectorizer(tweet_list_nopunct, stopwords=fr_stopwords, b_stemming=True, b_accent=False)
#f2 = open("vocs/voc2", "wb")
#pickle.dump(words_freq2, f2)
#f2.close()
#
#''' punctuation/stopwords/stemming/no accent'''
#[vectorizer3, words_freq3] = build_vectorizer(tweet_list,b_stemming=True, b_accent=False)
#f3 = open("vocs/voc3", "wb")
#pickle.dump(words_freq3, f3)
#f3.close()
#
#''' no punctuation/stopwords/stemming/no accent'''
#[vectorizer4, words_freq4] = build_vectorizer(tweet_list_nopunct,b_stemming=True, b_accent=False)
#f4 = open("vocs/voc4", "wb")
#pickle.dump(words_freq4, f4)
#f4.close()
#
#''' punctuation/no stopwords/no stemming/no accent'''
#[vectorizer5, words_freq5] = build_vectorizer(tweet_list,stopwords=fr_stopwords, b_accent=False)
#f5 = open("vocs/voc5", "wb")
#pickle.dump(words_freq5, f5)
#f5.close()
#
#''' no punctuation/no stopwords/no stemming/no accent'''
#[vectorizer6, words_freq6] = build_vectorizer(tweet_list_nopunct,stopwords=fr_stopwords, b_accent=False)
#f6 = open("vocs/voc6", "wb")
#pickle.dump(words_freq6, f6)
#f6.close()
#
#''' punctuation/stopwords/no stemming/no accent'''
#[vectorizer7, words_freq7] = build_vectorizer(tweet_list, b_accent=False)
#f7 = open("vocs/voc7", "wb")
#pickle.dump(words_freq7, f7)
#f7.close()
#
#''' no punctuation/stopwords/no stemming/no accent'''
#[vectorizer8, words_freq8] = build_vectorizer(tweet_list_nopunct, b_accent=False)
#f8 = open("vocs/voc8", "wb")
#pickle.dump(words_freq8, f8)
#f8.close()
