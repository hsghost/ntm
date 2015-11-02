#by Qian Ma
#take community detection by using CPM algorithm
#get inputs from sentiment analysis module
#save result in json

import networkx as nx
from twitterAPI import get_friends_followers_ids
from twitterLogin import oauth_login_1
import sa.sa
import time
import json
import MySQLdb

def communityDetection(twitter_api):


    #input from sentiment analysis module
    newtermList=sa.sa.sa_main(20) #[[word, pos, neg, freq],[]]

    #find target term to analyze
    target=[]
    for newterm in newtermList:
        group_size=len(newterm[1])+len(newterm[2])
        if group_size<=120: #group under such size can be handled in 2h
            target=newterm
            break

    if target==[]:
        return {}

    #return a dictionary containing graph information and communities
    result={}
    result['word']=target[0]
    result['positive_nodes'], result['positive_edges'], result['positive_communities']=singleDetection(twitter_api, target[1])
    result['negative_nodes'], result['negative_edges'], result['negative_communities']=singleDetection(twitter_api, target[2])

    return result

def singleDetection(twitter_api, group):
    #handle a single group

    #delete repeated user ids
    group=list(set(group))

    G=nx.Graph()

    #construct graph for the group by finding all the edges
    for user_id in group:
        friends_ids, followers_ids = get_friends_followers_ids(twitter_api, user_id=user_id)
        friends_ids_str=[str(friend_id) for friend_id in friends_ids]
        followers_ids_str=[str(follower_id) for follower_id in followers_ids]
        vertices = list(set(friends_ids_str) & set(group) & set(followers_ids_str)) #find nodes connected to current node in the group
        edges=[(str(user_id), vertex)for vertex in vertices]
        G.add_edges_from(edges)

    #find communites using CPM
    c=[]
    k=0
    for size in range(3,6):
        c_original=list(nx.k_clique_communities(G, size))
        if len(c_original)>0:
            c_listed=[list(froz) for froz in c_original]
            c=c_listed #if find communities using larger k, drop previous ones
            k=size
        else:
            break

    return G.nodes(), G.edges(), c


if __name__ == "__main__":

    twitter_api = oauth_login_1()
    conn=MySQLdb.connect(host="10.240.119.20",user="root",passwd="cis700fall2014",db="cis700",charset="utf8")
    cur = conn.cursor()
    while 1:
        result=communityDetection(twitter_api)

        if result=={}:
            continue
        temp_time=int(time.time())
        newterm_values=[temp_time, result['word']]
        cur.execute('UPDATE newterm SET analyzed_time=%s WHERE word=%s', newterm_values) #give a time stamp for the term analyzed
        conn.commit()

        #save result in json
        json.dump(result, open('communities/'+result['word']+'.dat', 'w'))

    cur.close()
    conn.close()

'''
json struct:

{
	'word': 'string'
	'positive_nodes': []
	'positive_edges': [(,), (,),  ...]
	'positive_communities': [[], [], ...]
	'negative_nodes': []
	'negative_edges': [(,), (,),  ...]
	'negative_communities': [[], [], ...]
 }
'''
