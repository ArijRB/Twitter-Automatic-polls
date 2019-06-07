import sys
sys.path.insert(0, '../src')
from utils import *

twitter_db = connect_to_db()
cursor = twitter_db.cursor()
query = "SELECT text, tweet_id FROM tweets WHERE lang='fr'"
cursor.execute(query)

for (text, tweet_id) in cursor.fetchall():
    cursor2 = twitter_db.cursor()
    formatted_text = format_punctuation(text)
    print(tweet_id)
    sql = """UPDATE tweets SET text_punct = \"%s\" WHERE tweet_id = %s"""
    val = (formatted_text, tweet_id)
    cursor2.execute(sql, val)
    cursor2.close()
    twitter_db.commit()

print("{} record(s) affected".format(cursor.rowcount))
cursor.close()
twitter_db.close()




