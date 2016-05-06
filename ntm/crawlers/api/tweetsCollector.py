#by Qian Ma

import twitter
import time
import MySQLdb
from wordFilter import wordFilter
from twitterLogin import oauth_login_0


twitter_api = oauth_login_0()
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

#location, temply concentrate on NYC
loc='-74,40,-73,41'

conn=MySQLdb.connect(host="10.240.119.20",user="root",passwd="cis700fall2014",db="cis700",charset="utf8")
cur = conn.cursor()

#use steaming api
stream = twitter_stream.statuses.filter(locations=loc)

wf = wordFilter(conn, cur)
newWords = []

for tweet in stream:

    #use filter to check if the tweet contains new terms
    newWords = wf.filterAll(tweet['text'])
    if newWords == []:
        continue

    temp_time=int(time.time())

    sign=0
    newWords=list(set(newWords))
    for word in newWords:
        if word not in tweet['text']:
            continue
        sign=1
        term_value=[word, 1, temp_time]

        #insert in new term or add to the refered count
    	cur.execute('INSERT INTO newterm (word, count, time) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE count=count+1', term_value)

        #construct the relation between tweets with the new terms contained
    	relation_value=[tweet['id'],word]
        cur.execute('INSERT INTO tweets_newterm VALUES (%s,%s)', relation_value)

        #print word,' : ',tweet['text']

    if sign==1:
        tweet_value=[tweet['id'], temp_time, tweet['user']['id'], tweet['text']]
        cur.execute('INSERT INTO tweets VALUES (%s,%s, %s, %s)',tweet_value)

    conn.commit()



cur.close()
conn.close()





