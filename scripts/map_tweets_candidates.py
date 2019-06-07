import sys
sys.path.insert(0, '../src')
from utils import *
import numpy as np

'''
    (from the most to the least significant bit)
    1 : Nathalie Arthaud
    2 : François Asselineau
    3 : Jacques Cheminade
    4 : Nicolas Dupont-Aignan
    5 : François Fillon
    6 : Benoît Hamon
    7 : Jean Lassalle
    8 : Marine Le Pen
    9 : Emmanuel Macron
    10 : Jean-Luc Mélenchon
    11 : Philippe Poutou
'''

twitter_db = connect_to_db()
cursor = twitter_db.cursor()
### columns have already been added to table tweets
query = "SELECT text, tweet_id FROM tweets WHERE lang='fr'"
cursor.execute(query)

for (text, tweet_id) in cursor.fetchall():
    cursor2 = twitter_db.cursor()
    bits = np.zeros(11)
    text = remove_accents(text)

    if re.findall(r"(nathalie|arthaud|n_arthaud)",text,re.IGNORECASE):
        bits[0] = 1
    if re.findall(r"(asselineau|upr_asselineau|upr)",text,re.IGNORECASE):
        bits[1] = 1
    if re.findall(r"(jacques|cheminade|jcheminade)",text,re.IGNORECASE):
        bits[2] = 1
    if re.findall(r"(dupont-aignan|dupont|aignan|nicolas dupont-aignan)",text,re.IGNORECASE):
        bits[3] = 1
    if re.findall(r"(fillon|(?<=#)lr|\blr\b)",text,re.IGNORECASE):
        bits[4] = 1
    if re.findall(r"(benoit|hamon|(?<=#)ps|(?<!\w)ps)",text,re.IGNORECASE):
        bits[5] = 1
    if re.findall(r"(lassalle)",text,re.IGNORECASE):
        bits[6] = 1
    if re.findall(r"(le pen|lepen|marine|mlp|front national|fn|frontnational)",text,re.IGNORECASE):
        bits[7] = 1
    if re.findall(r"(emmanuel|macron|enmarche)",text,re.IGNORECASE):
        bits[8] = 1
    if re.findall(r"(jlm|jean-luc|melenchon|jlmelenchon|jean luc|franceinsoumise|france insoumise)",text,re.IGNORECASE):
        bits[9] = 1
    if re.findall(r"(poutou|philippe poutou)",text,re.IGNORECASE):
        bits[10] = 1

    bits = ''.join([str(int(b)) for b in bits])
    sql = """UPDATE tweets SET candidates = %s WHERE tweet_id = %s"""
    val = (bits, tweet_id)
    cursor2.execute(sql, val)
    cursor2.close()
    twitter_db.commit()
    print(tweet_id)

print("{} record(s) affected".format(cursor.rowcount))
cursor.close()
twitter_db.close()


