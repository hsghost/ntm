# -*- coding: utf-8 -*-
"""
Module wordFilter
Version 1.2

CIS 700 M004 - Social Media Mining
Fall 2014 Term Project

Last modified Dec 14, 2014

@author: Aifeng Yun

    This module is intended for screening out the "new words" from the tweets
    obtained by the data collection module. It will first check the word in
    a local vocabulary table (cache), if missed, it will call the udQuery
    module to do a remote check through Urban Dictionary API. If the query
    returns true, it will add the word into the local vocabulary table to mark
    it as "known", hence further encounter of the word can be filtered locally.
    Otherwise, it will mark the word as "new" and return it to the caller.

"""

import re
from nltk.tokenize import sent_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.util import bigrams,trigrams
from udQuery import udQuery

knownWordsList = [u'requires', u'3rd', u'closely', u'purchasing', u'combined',
                  u'saying', u'noticed', u'watching', u'center', u'filled',
                  u'closely' ,u'afraid', u'following', u'moved', u'certificate'
                  u'unsettling', u'investigations', u'looked', u'hour']

class wordFilter:
    text = ''
    words = []
    filteredWords = []
    filteredPhrases = []
    filteredAll = []
    sentences = []
    (db, dbc) = (None, None)
    udq = None
    unicodeReg = r'[^\x00-\x7f]+'
    unicodeRepl = r'_'
    linkReg = r'(?:\b(?:http)+?s*?:+?(?://)+?(?:\S*\b)*)|(?:(?:\b\w+)*?@+?\w+(?:\.+?\w+)*\b)'
    dotAcroReg = r'\.(?!(\S[^. ])|\d)'
    dotAcroRepl = r''
    underscoreReg = r'_+'
    underscoreRepl = r' '
    hashtagReg = r'#+?\w+\b'
    hashtagRepl = r''
    aposReg = r'(?:\b\w+)*\'+?(?:\w+\b)*'
    stopwordsReg = r''
    knownwordsReg = r''
    splittingReg = r'\W'
    emptyStr = ''

    def __init__(self, db, dbc, udq = udQuery(), stopwordsList = stopwords.words('english'), knownwordsList = knownWordsList):
        (self.db, self.dbc) = (db, dbc)
        self.udq = udq
        self.stopwordsReg = r'\b(?:' + '|'.join(stopwordsList) + r')+\b'
        self.knownwordsReg = r'\b(:' + '|'.join(knownwordsList) + r')+\b'

    def filterWords(self):
        self.filteredWords = []
        self.text = re.sub(self.aposReg, self.emptyStr, self.text)
        self.words = list(set(filter(None, re.split(self.splittingReg, self.text.lower()))))
        for word in self.words:
            if self.dbc.execute("SELECT 1 FROM vocabulary WHERE term = %s LIMIT 1;", word) == 0L:
                if self.udq.recorded(word):
                    if len(word) <= 140:
                        self.dbc.execute("INSERT INTO vocabulary (term) VALUE (%s)", word)
                else:
                    self.filteredWords.append(word)
        return self.filteredWords

    def filterPhrases(self):
        self.filteredPhrases = []
        self.sentences = sent_tokenize(self.text)
        for sentence in self.sentences:
            bigramList = list(set(bigrams(wordpunct_tokenize(sentence.lower()))))
            for bigram in bigramList:
                (word1, word2) = bigram
                if word1 == "'":
                    term = word1 + word2
                elif re.match(r'\W+', word1) == None and re.match(r'\W+', word2) == None:
                    term = word1 + ' ' + word2
                else:
                    continue
                if self.dbc.execute("SELECT 1 FROM vocabulary WHERE term = %s LIMIT 1;", term) == 0L:
                    if self.udq.recorded(term):
                        if len(term) <= 140:
                            self.dbc.execute("INSERT INTO vocabulary (term) VALUE (%s)", term)
                    else:
                        self.filteredPhrases.append(term)
            trigramList = list(set(trigrams(wordpunct_tokenize(sentence.lower()))))
            for trigram in trigramList:
                (word1, word2, word3) = trigram
                if word3 == "'":
                    continue
                elif word2 == "'":
                    term = word1 + word2 + word3
                elif re.match(r'\W+', word1) == None and re.match(r'\W+', word2) == None and re.match(r'\W+', word3) == None:
                    term = word1 + ' ' + word2 + ' ' + word3
                else:
                    continue
                if self.dbc.execute("SELECT 1 FROM vocabulary WHERE term = %s LIMIT 1;", term) == 0L:
                    if self.udq.recorded(term):
                        if len(term) <= 140:
                            self.dbc.execute("INSERT INTO vocabulary (term) VALUE (%s)", term)
                    else:
                        self.filteredPhrases.append(term)
        return self.filteredPhrases

    def filterAll(self, text):
        self.text = re.sub(self.unicodeReg, self.unicodeRepl, text)
        self.text = re.sub(self.linkReg, self.emptyStr, self.text)
        self.text = re.sub(self.hashtagReg, self.hashtagRepl, self.text)
        self.text = re.sub(self.dotAcroReg, self.dotAcroRepl, self.text)
        self.text = re.sub(self.underscoreReg, self.underscoreRepl, self.text)
        self.text = re.sub(self.stopwordsReg, self.emptyStr, self.text)
        self.text = re.sub(self.knownwordsReg, self.emptyStr, self.text)

        self.filteredAll.extend(self.filterWords())
#        self.filteredAll.extend(self.filterPhrases())

        return self.filteredAll

#==============================================================================
#     def splitHashtag(self, hashtag):
#         self.dbc.execute("SELECT * FROM V")
#
#==============================================================================
