import mysql.connector
import numpy as np

def connect_to_db():
    '''
        establishes a session with the MySQL server

        returns
        ------
        twitter_db : mysql.connector.MySQLConnection
                     connection with the MySQL server

    '''
    twitter_db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        database="twitter_db"
    )
    return twitter_db

def get_tweets(N=None, keep_retweets=False, keep_punctuation=True):
    '''
        connects to the database and retrieves tweets

        parameters
        ----------
        N : int (default : None)
            maximum number of tweets to retrieve
        keep_retweets : boolean (default : False)
                        True if retweets are to be kept, False otherwise
        keep_punctuation : boolean (default : True)
                           True if punctuation is to be kept, False otherwise
        returns
        -------
        tweets : np.array, shape (n_tweets, )
                 tweets retrieved with the above parameters
    '''
    twitter_db = connect_to_db()
    tweet_list = []
    cursor = twitter_db.cursor()

    if N:
        limit = " LIMIT " + str(N)
    else:
        limit = ""

    if keep_punctuation:
        text = "text_punct"
    else:
        text = "text"

    if keep_retweets:
        query = "SELECT " + text + " FROM tweets WHERE lang='fr'" + limit
    else:
        query = "SELECT " + text + " FROM tweets WHERE NOT (text LIKE '%RT @%') AND lang='fr'" + limit

    cursor.execute(query)

    for text in cursor:
        tweet_list.append(text[0])

    cursor.close()
    tweets = np.array(tweet_list)
    return tweets

def get_tweets_from_user(user_id, N=None, keep_retweets=False, keep_punctuation=True):
    '''
        retrieves from twitter_db a specific user's tweets

        parameters
        ----------
        user_id : int
                  user identifier
        N : int (default : None)
            maximum number of tweets to retrieve
        keep_retweets : boolean (default : False)
                        True if retweets are to be kept, False otherwise
        keep_punctuation : boolean (default : True)
                           True if punctuation is to be kept, False otherwise
        returns
        -------
        tweets : np.array, shape (n_tweets,)
                 (N first) tweets from user identified by user_id
    '''
    twitter_db = connect_to_db()
    tweet_list = []
    cursor = twitter_db.cursor()

    if N:
        limit = "LIMIT " + str(N)
    else:
        limit = ""

    if not keep_retweets:
        s_remove_retweets = "AND NOT (text LIKE '%RT @%') "
    else:
        s_remove_retweets = ""

    query = "SELECT text FROM tweets WHERE user_id = " + str(user_id) +" AND lang='fr' " + s_remove_retweets + limit
    cursor.execute(query)

    for text in cursor:
        tweet_list.append(text[0])

    cursor.close()
    tweets = np.array(tweet_list)
    return tweets

def get_tweets_and_sentiments_from_user(user, candidate, N=None, keep_retweets=False, keep_punctuation=True):
    '''
        retrieves from twitter_db a specific user's tweets and associates each
        tweet to its sentiment (positive if candidate is mentioned, negative otherwise)
        removes those that mention :
        - no candidate
        - or several candidates including specific one

        parameters
        ----------
        user_id : int
                  user identifier
        candidate : int
                    candidate supported by user
        N : int (default : None)
            maximum number of tweets to retrieve
        keep_retweets : boolean (default : False)
                        True if retweets are to be kept, False otherwise
        keep_punctuation : boolean (default : True)
                           True if punctuation is to be kept, False otherwise
        returns
        -------
        tweets : np.array, shape (n_tweets,)
                 (N first) tweets from user identified by user_id
    '''
    twitter_db = connect_to_db()
    tweet_list = []
    sentiment_list = []
    cursor = twitter_db.cursor()

    if N:
        limit = "LIMIT " + str(N)
    else:
        limit = ""

    if not keep_retweets:
        s_remove_retweets = "AND NOT (text LIKE '%RT @%') "
    else:
        s_remove_retweets = ""

    query = "SELECT text, candidates FROM tweets WHERE user_id = " + str(user) +" AND lang='fr' " + s_remove_retweets + limit
    cursor.execute(query)

    for res in cursor:
        text = res[0]
        candidates = np.array(list(res[1])).astype(int)
        mentioned = np.argwhere(candidates == 1).flatten()

        # tweet mentions specified candidate -> positive sentiment
        if len(mentioned == 1) and mentioned[0] == candidate:
            tweet_list.append(text)
            sentiment_list.append(1)
        # tweet mentions other candidates -> negative sentiment
        elif len(mentioned > 1) and candidate not in mentioned:
            tweet_list.append(text)
            sentiment_list.append(-1)

    cursor.close()
    tweets = np.array(tweet_list)
    sentiments = np.array(sentiment_list)
    return tweets, sentiments

def mentioned_candidates_from_mult_users(users, N=None, keep_retweets=False):
    '''
        from twitter_db, retrieves candidates that are mentioned in each
        tweet posted by specific users

        parameters
        ----------
        users : int list
                list of users, identified by their id
        N : int
            maximum number of tweets to extract
        keep_retweets : boolean (default : False)
                        True if retweets are to be kept, False otherwise
        returns
        -------
        candidates : np.array, shape (n_tweets, 11)
                     mentioned candidates in each tweet
    '''
    twitter_db = connect_to_db()
    cursor = twitter_db.cursor()

    if N:
        limit = " LIMIT " + str(N)
    else:
        limit = ""

    if not keep_retweets:
        s_remove_retweets = "AND NOT (text LIKE '%RT @%') "
    else:
        s_remove_retweets = ""

    query = "SELECT candidates\
            FROM tweets\
            WHERE lang='fr' " + s_remove_retweets + "AND \
            (user_id IN " + str(users) + " OR \
            in_reply_to_user_id IN " + str(users) + " OR \
            quoted_user_id IN " + str(users) + " OR \
            retweeted_user_id IN " + str(users) + ")" + limit

    #query = "SELECT candidates\
    #        FROM tweets\
    #        WHERE lang='fr' " + s_remove_retweets + "AND \
    #        user_id IN " + str(users) + limit

    cursor.execute(query)

    #tweets = []
    candidates = []
    #for tweet, cand in cursor:
    for cand in cursor:
        #tweets.append(tweet)
        candidates.append(list(cand[0])) # string of 0 and 1 -> list of 0 and 1
    cursor.close()

    # cast to int
    candidates = np.array(candidates).astype(int)
    #return tweets, candidates
    return candidates

def mentioned_candidates_from_user(user_id, N=None, keep_retweets=False):
    '''
        from twitter_db, retrieves candidates that are mentioned in each
        tweet involving a specific user

        parameters
        ----------
        users : int list
                list of users, identified by their id
        N : int
            maximum number of tweets to extract
        keep_retweets : boolean (default : False)
                        True if retweets are to be kept, False otherwise
        returns
        -------
        candidates : np.array, shape (n_tweets, 11)
                     mentioned candidates in each tweet
    '''
    twitter_db = connect_to_db()
    cursor = twitter_db.cursor()

    if N is None:
        limit = ""
    else:
        limit = " LIMIT " + str(N)

    if not keep_retweets:
        s_remove_retweets = "AND NOT (text LIKE '%RT @%') "
    else:
        s_remove_retweets = ""

    ''' ---> À VÉRIFIER '''
    query = "SELECT candidates\
            FROM tweets\
            WHERE lang='fr' " + s_remove_retweets + "AND \
            (user_id = " + str(user_id) + " OR \
            in_reply_to_user_id = " + str(user_id) + " OR \
            quoted_user_id = " + str(user_id) + " OR \
            retweeted_user_id = " + str(user_id) + ")" + limit

    #query = "SELECT candidates\
    #        FROM tweets\
    #        WHERE lang='fr' " + s_remove_retweets + "AND \
    #        user_id = " + str(user_id) + limit

    cursor.execute(query)

    candidates = []
    for cand in cursor:
        candidates.append(list(cand[0])) # string of 0 and 1 -> list of 0 and 1
    cursor.close()

    # cast to int
    candidates = np.array(candidates).astype(int)
    return candidates

def get_nb_tweets_per_user(users):
    '''
        from twitter_db, retrieves total number of tweets posted by each
        specified user

        parameters
        ----------
        users : int list
                list of users, identified by their id
        returns
        -------
        nb_tweets_per_user : dict of int -> int
                             dictionary mapping each user in users to his/her
                             number of tweets
    '''
    nb_tweets_per_user = dict()
    twitter_db = connect_to_db()
    for user in users:
        cursor = twitter_db.cursor()
        query = "SELECT COUNT(*) FROM tweets WHERE lang='fr' AND user_id = " + str(user)
        cursor.execute(query)
        nb_tweets_per_user[user] = cursor.fetchall()[0][0]
        cursor.close()
    return nb_tweets_per_user

def get_nb_retweets_per_user(users, keep_retweets=False):
    '''
        from twitter_db, retrieves number of retweets posted by each
        specified user

        parameters
        ----------
        users : int list
                list of users, identified by their id
        returns
        -------
        nb_retweets_per_user : dict of int -> int
                             dictionary mapping each user in users to his/her
                             number of tweets
    '''
    nb_retweets_per_user = dict()
    twitter_db = connect_to_db()
    for user in users:
        cursor = twitter_db.cursor()
        query = "SELECT COUNT(*) FROM tweets WHERE user_id = " + str(user) + " AND text LIKE '%RT @%'"
        cursor.execute(query)
        nb_retweets_per_user[user] = cursor.fetchall()[0][0]
        cursor.close()
    return nb_retweets_per_user

def get_ratio_retweets_per_user(users):
    '''
        from twitter_db, for each specified user, retrieves the ratio
        between retweets and tweets (retweets included)

        parameters
        ----------
        users : int list
                list of users, identified by their id
        N : int
            maximum number of tweets to extract
        keep_retweets : boolean (default : False)
                        True if retweets are to be kept, False otherwise
        returns
        -------
        ratio_per_user : dict of int -> float
                         dictionary mapping each user in users to his/her
                         ratio
    '''

    ratio_per_user = dict()
    nb_tweets_per_user = get_nb_tweets_per_user(users)
    nb_retweets_per_user = get_nb_retweets_per_user(users)

    for u in users:
        ratio_per_user[u] = nb_retweets_per_user[u] / nb_tweets_per_user[u]

    return ratio_per_user


