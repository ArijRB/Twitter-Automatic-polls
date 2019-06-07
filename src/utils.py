from preprocessing import *
from query_tools import *
from parsing import *
from community_graph import *
import pickle

candidates_mapping = {
    0 : "Arthaud",
    1 : "Asselineau",
    2 : "Cheminade",
    3 : "Dupont-Aignan",
    4 : "Fillon",
    5 : "Hamon",
    6 : "Lassalle",
    7 : "Le Pen",
    8 : "Macron",
    9 : "Mélenchon",
    10 : "Poutou"
}

candidate_color_mapping = {
    0 : "#f58231", # Arthaud -> orange
    1 : "#808000", # Asselineau -> olive
    2 : "#9A6324", # Cheminade -> brown
    3 : "#800000", # Dupont-Aignan -> maroon
    4 : "green", # Fillon
    5 : "yellow", # Hamon
    6 : "magenta", # Lassalle
    7 : "#000075", # Le Pen -> navy
    8 : "blue", # Macron
    9 : "red", # Mélenchon
    10 : "purple" # Poutou
}

def get_ratio_retweets_per_user(users_list):
    ratio_per_user = dict()
    nb_tweets_per_user = get_nb_tweets_per_user(users_list)
    nb_retweets_per_user = get_nb_retweets_per_user(users_list)

    for user, nb in nb_tweets_per_user.items():
        if nb > 0:
            ratio_per_user[user] = nb_retweets_per_user[user] * 1.0 / nb

    return ratio_per_user

def save_object(obj, filename):
    '''
        saves object to file

        parameters
        ----------
        obj : Object
              any kind of pickeable object
        filename : string
                   file name where object is to be stored
    '''
    f = open(filename, 'wb')
    pickle.dump(obj, f)
    f.close()
    print("Saved object to file {}".format(filename))






