#!/usr/bin/python

import nltk
import nltk.data
from nltk.util import ngrams

from nltk.tokenize import word_tokenize

import MySQLdb

mHost = "10.240.119.20"
mUser = "root"
mPasswd = "cis700fall2014"
mDb = "cis700"
mCharset = "utf8"
conn = MySQLdb.connect(host=mHost,user=mUser,passwd=mPasswd,db=mDb,charset=mCharset)
cur = conn.cursor()

classifier = nltk.data.load("classifiers/movie_reviews_NaiveBayes.pickle")

def sa_text (raw_text):
    dtext = raw_text.decode('utf-8')
    text = word_tokenize(dtext)
    feats = dict([(word, True) for word in text + list(ngrams(text, 2))])
    return classifier.classify(feats)

# @param tweet_id
# @return sentiment towords it

def sa_by_tweet_id (tweet_id):
    cur.execute("select content from tweets where id=%s", tweet_id)
    res = cur.fetchall()
    if len(res) == 0:
        return "nul"

    tweet_text = res[0]
    return sa_text(tweet_text[0])

def get_uid (tweet_id):
    cur.execute("select user from tweets where id=%s", tweet_id)
    res = cur.fetchall()
    if len(res) == 0:
        return "nul"

    return res[0]


def sa_on_word (word):
    cur.execute("select id from tweets_newterm where word=%s", word)
    res = cur.fetchall()

    pos = []
    neg = []
    for tid in res:
        sent = sa_by_tweet_id(tid)
        uid = get_uid(tid)
        if sent == "pos":
            pos += uid
        elif sent == "neg":
            neg += uid
    ret = [word, pos, neg]
    return ret

# main entry
# get top 'num' of new term and do SA
# @para num
# @return list[word, pos, neg]

def sa_main(num = 20):
    cur.execute("select word,freq from newterm where count>10 and analyzed_time=0 order by freq DESC limit %s", num)
    res = cur.fetchall()

    sa = []
    for r in res:
        sow=sa_on_word(r[0])
        sow.append(r[1])
        sa.append(sow)

    print sa
    return sa

# print sa_main(10)
