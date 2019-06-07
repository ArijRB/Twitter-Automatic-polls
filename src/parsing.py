import os
from lxml import etree
import pandas as pd
from random import shuffle

def parse_decathlon():
    '''
        parse and return dataframe containing decathlon reviews
    '''
    path = 'data/decathlon/'

    repos = os.listdir(path)
    parser = etree.XMLParser(recover=True)
    t=[]
    for repo in repos:
        if os.path.isdir(path+repo):
            files = os.listdir(path+repo)
            for name in files:
                file=etree.parse(path+repo+"/"+name, parser=parser)
                avis=file.xpath("./avis")
                for av in avis:
                    d=dict()
                    if len(av.xpath("./commentaire/text()")) == 0 or len(av.xpath("./note/text()")) == 0:
                        continue

                    d["score"]=int(av.xpath("./note/text()")[0])
                    if d["score"]==3:
                        continue
                    #add label +1 -1 by score
                    if d["score"] >3:
                        d["label"]=+1
                    else:
                        d["label"]=-1
                    d["review"]=av.xpath("./commentaire/text()")[0]

                    t.append(d)

    df = pd.DataFrame.from_records(t)
    df.to_csv('csv/decathlon_reviews.csv',index=False)
    return df

def parse_movies():
    path = "data/movies"
    dir_pos = path + "/pos/"
    dir_neg = path + "/neg/"
    files_pos = os.listdir(dir_pos)
    files_neg = os.listdir(dir_neg)
    t = []
    for fname in files_pos:
        d = dict()
        file = open(dir_pos + fname, "r", encoding="utf-8")
        content = file.readlines()[4:]
        content = ' '.join(content)
        d['review'] = content
        d['label'] = +1
        t.append(d)
    for fname in files_neg:
        d = dict()
        file = open(dir_neg + fname, "r", encoding="utf-8")
        content = file.readlines()[4:]
        content = ' '.join(content)
        d['review'] = content
        d['label'] = -1
        t.append(d)
    shuffle(t)
    df = pd.DataFrame.from_records(t)
    df.to_csv('csv/movie_reviews.csv',index=False)
    return df



