import sys
sys.path.insert(0, '../src')
from query_tools import *

twitter_db = connect_to_db()
cursor = twitter_db.cursor()
query = ("SELECT retweeted_status_id \
        FROM tweets \
        WHERE NOT (retweeted_status_id IS NULL) \
            AND retweeted_status_id NOT IN \
                (SELECT tweet_id FROM tweets);")
cursor.execute(query)

f = open("misc/unknown_retweeted_tweets.txt", "w")
for retweeted_status_id in cursor:
    print(retweeted_status_id[0])
    f.write("%s\n" % retweeted_status_id[0])
cursor.close()

f.close()

