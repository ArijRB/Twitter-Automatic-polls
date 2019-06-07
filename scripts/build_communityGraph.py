import sys
sys.path.insert(0, '../src')
from utils import *
import pandas as pd
from collections import Counter
import pickle

"""
    This script :
    - builds a community graph based on a specified amount of tweets
    - links each of the biggest communities to its candidate
    - extract tweets from each community to create a labeled dataset
"""

N = 10000
CENTRALITY_THRESHOLD = 0.005
PLOT_GRAPHS = False
PLOT_HISTS = False


def build_communityGraph(version, N):
    '''
        generates a community graph based on a sample of N tweets and Louvain algorithm
        and saves original graph, partition, layout and number of tweets per user - as
        pickable objects - to their respective files

        parameters
        ----------
        version : string
                  version number
        N : int
            number of tweets to retrieve

        returns
        -------
        G : networkx.DiGraph
            graph
        partition : dict of int -> int
                    dictionary mapping each user to his community
        layout : dict of int -> (float, float)
                 dictionary of node positions
        nb_tweets_per_user : dict of int -> int
                             dictionary mapping each user to his number
                             of tweets
    '''
    G_dict, G = create_graph(N)

    # apply Louvain algorithm
    G_undirected = nx.Graph(G) # necessary to apply Louvain algorithm
    partition = community_louvain.best_partition(G_undirected)
    print("Computed partition")
    layout = community_layout(G_undirected, partition)
    print("Computed community layout")

    # adjust node size according to user's number of tweets
    all_users = list(partition.keys())
    nb_tweets_per_user = get_nb_tweets_per_user(all_users)

    # save to files
    f_graph = "../communities/v{}/graph".format(version)
    f_partition = "../communities/v{}/partition".format(version)
    f_layout = "../communities/v{}/layout".format(version)
    f_nb = "../communities/v{}/nb_tweets_per_user".format(version)
    save_object(G, f_graph)
    save_object(partition, f_partition)
    save_object(layout, f_layout)
    save_object(nb_tweets_per_user, f_nb)
    return G, partition, layout, nb_tweets_per_user

def assign_community_to_candidate(version, G, partition, nb_tweets_per_user):
    '''
        assigns each of the biggest communities to its candidate

        parameters
        ----------
        version : string
                  version number
        G : networkx.DiGraph
            graph
        partition : dict of int -> int
                    dictionary mapping each user to his community
        layout : dict of int -> (float, float)
                 dictionary of node positions
        nb_tweets_per_user : dict of int -> int
                             dictionary mapping each user to his number
                             of tweets
        returns
        -------
        candidate_to_community : list of int -> np.array, shape (n_users, 2)
                                 dictionary mapping a candidate to its community
    '''
    values = list(partition.values())
    # for each community, count number of users belonging to it
    # and sort communities in descending order with respect to their number of users
    c = Counter(values)
    communities_id_sorted = sorted(np.unique(values), key=c.get, reverse=True)

    # create array where first column = community, second column = size of community
    communities_counts = [(community_id, c[community_id]) for community_id in communities_id_sorted]
    communities_counts = np.array(communities_counts)

    # keep communities that contain more than 100 nodes
    communities_filtered = communities_counts[np.where(communities_counts[:,1] >= 100)][:,0]
    k = len(communities_filtered)
    print("Keeping the following communities : {}".format(communities_filtered))

    # remove parts of the graph that are unrelated to these communities
    partition_filtered, G_filtered, nb_tweets_per_user_filtered = filter_graph_community\
                                                        (partition, G, \
                                                        nb_tweets_per_user,\
                                                        communities_filtered)
    print("Built new graph based on these communities")

    # compute new graph layout
    pos = community_layout(G_filtered, partition_filtered)
    print("Computed new graph layout based on these communities")

    plot_community_graph(G_filtered, pos, partition_filtered, nb_tweets_per_user_filtered,\
            filename="../communities/v" + str(version) + "/plot_biggest_communities")

    # create array out of partition_filtered
    partition_filtered_array = np.array([(user_id, community) for (user_id, community) in partition_filtered.items()])

    # create array out of nb_tweets_per_user
    nb_tweets_filtered_array = np.array([(user_id, nb) for (user_id, nb) in nb_tweets_per_user_filtered.items()])

    # element i of communities is the subarray of partition_filtered_array corresponding to the ith biggest community
    communities = []
    for i in range(k):
        com = partition_filtered_array[np.where\
                (partition_filtered_array[:,1] == communities_filtered[i])]
        communities.append(com)

    # dictionary mapping community to its candidate
    candidate_to_community = dict()
    mapped = np.zeros(11) # 0 if candidate is not mapped to its community, 1 elsewise

    for i in range(k):
        # get users from ith biggest community
        users = communities[i][:,0]
        # compute average number of tweets among this community
        avg = np.mean(nb_tweets_filtered_array[np.where(np.in1d(nb_tweets_filtered_array[:,0],\
                users))][:,1])
        candidates = mentioned_candidates_from_mult_users(tuple(users),10000,keep_retweets=True)
        cand = np.argmax(np.sum(candidates, axis=0))

        if mapped[cand] == 0:
            candidate_to_community[cand] = communities[i]
            mapped[cand] = 1

        print("Community {} - average number of tweets per user : {} - \
                most mentioned candidate : {}".format(communities_filtered[i], \
                avg, candidates_mapping[cand]))

    for k,v in candidate_to_community.items():
        print("{} -> community {}".format(candidates_mapping[k], v[0][1]))

    # save to files
    f_cand_to_comm = "../communities/v{}/candidate_to_community".format(version)
    save_object(candidate_to_community, f_cand_to_comm)
    return candidate_to_community

def create_corpus(version, G, partition, nb_tweets_per_user, candidate_to_community):
    '''
        for each community, retrieve users' tweets in order to create a labeled dataset

        parameters
        ----------
        version : string
                  version number
        G : networkx.DiGraph
            graph
        partition : dict of int -> int
                    dictionary mapping each user to his community
        layout : dict of int -> (float, float)
                 dictionary of node positions
        nb_tweets_per_user : dict of int -> int
                             dictionary mapping each user to his number
                             of tweets
        candidate_to_community : list of int -> np.array, shape (n_users, 2)
                                 dictionary mapping a candidate to its community
        returns
        -------
        candidate_to_users : dict of int -> int list
                            dictionary mapping candidates to the users that support them
        corpus : dict of int -> ((np.array, shape (n_users, )), (np.array, shape(n_users,))
                 dictionary mapping candidates to their representative tweets
    '''
    candidate_to_users = dict()

    # remove users that only retweet
    for cand, community in candidate_to_community.items():
        users = community[:,0]
        nb_retweets_per_user = get_ratio_retweets_per_user(users)
        nb_retweets_per_user = np.array([(user, ratio) for user, ratio in nb_retweets_per_user.items()])
        to_keep = nb_retweets_per_user[np.where(nb_retweets_per_user[:,1] < 1)][:,0]
        candidate_to_users[cand] = to_keep
        print("{} - number of bots among {} users : {}".format(candidates_mapping[cand], len(users), len(users) - len(to_keep)))

    corpus = dict()

    for cand, users in candidate_to_users.items():
        print(cand)
        fname_graph = "../communities/v{}/plot_community_{}".format(version, candidates_mapping[cand])
        fname_hist = "../communities/v{}/hist_centrality_{}".format(version,candidates_mapping[cand])
        partition_cand, G_cand, nb_tweets_cand = filter_graph_users(partition, G, nb_tweets_per_user, users)

        dict_centrality = nx.degree_centrality(G_cand)

        if PLOT_HISTS:
            # save histogram
            save_hist(list(dict_centrality.values()), filename=fname_hist)

        # set threshold to eliminate users that do not sufficiently belong to the community
        dict_centrality_filtered = {k:v for k,v in dict_centrality.items() if v > CENTRALITY_THRESHOLD}
        users_to_keep = list(dict_centrality_filtered.keys())

        # update community
        candidate_to_users[cand] = users_to_keep

        if PLOT_GRAPHS:
            users_color = get_nodes_color(users_to_keep)

            partition_cand, G_cand, nb_tweets_cand = filter_graph_users(partition, \
                    G, nb_tweets_per_user, users_to_keep)
            pos_cand = community_layout(G_cand, partition_cand)
            # save plot
            plot_community_graph(G_cand, pos_cand, partition_cand, nb_tweets_cand, \
                    dict_node_color=users_color, filename=fname_graph)

        # get 50 tweets (retweets not included) from each user
        tweets = []
        sentiments = []
        for user in users_to_keep:
            t, s = get_tweets_and_sentiments_from_user(user, cand, N=50)
            tweets = np.append(tweets, t)
            sentiments = np.append(sentiments, s)
        corpus[cand] = (tweets, sentiments)

        print("Computed corpus for {}".format(candidates_mapping[cand]))

    f_cand_to_users = "../communities/v{}/candidate_to_users".format(version)
    save_object(candidate_to_users, f_cand_to_users)

    f_cand_to_tweets = "../communities/v{}/candidate_to_tweets".format(version)
    save_object(corpus, f_cand_to_tweets)

    return candidate_to_users, corpus

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Missing argument : version number required")
    else:
        try:
            VERSION = sys.argv[1]
            G, partition, layout, nb_tweets_per_user = build_communityGraph(VERSION, N)
            candidate_to_community = assign_community_to_candidate(VERSION, G, partition, nb_tweets_per_user)

            if len(sys.argv) > 2:
                if sys.argv[2] == '1':
                    PLOT_GRAPHS = True
                elif sys.argv[2] == '2':
                    PLOT_HISTS = True
                elif sys.argv[2] == '3':
                    PLOT_GRAPHS = True
                    PLOT_HISTS= True
            candidate_to_users, candidate_to_tweets = create_corpus(VERSION, G, partition, nb_tweets_per_user, candidate_to_community)

        except ValueError:
            print("Type error : version number needs to be an integer")



