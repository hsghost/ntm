# -*- coding: utf-8 -*-
"""
Module wordRcmd
Version 1.0

CIS 700 M004 - Social Media Mining
Fall 2014 Term Project

Last modified Dec 14, 2014

@author: Aifeng Yun

    TODO: Module Description.
    
"""

import sys
import json

class wordRcmd:
    (db, dbc) = (None, None)
    (lTh, hTh) = (0, 100)
    (lPc, hPc) = (0, 1)
    cycle = 30
    hotWords = []
    hotWordUsers = {}
    candidWords = []
    newWordUsers = []
    rcmdWords = []
    jsonFile = None
    jsonData = None
    (posNodes, negNodes) = ([], [])
    
    def __init__(self, db, dbc, lowThreshold, highThreshold, lowPercentage, highPercentage, updateCycle):
        (self.db, self.dbc) = (db, dbc)
        (self.lTh, self.hTh) = (lowThreshold, highThreshold)
        (self.lPc, self.hPc) = (lowPercentage, highPercentage)
        self.cycle = updateCycle
    
    def recommendWords(self, hotwords):
        (self.candidWords, self.rcmdWords) = ([], [])
        (self.jsonFile, self.jsonData) = (None, None)
        (self.posNodes, self.negNodes) = ([], [])
        self.hotWords = hotwords
        for hWord in self.hotWords:
            try:
                self.jsonFile = open('communities/' + hWord +'.dat', 'r')
                self.jsonData = json.load(self.jsonFile.read().decode('utf-8'))
            except Exception:
                continue
            (self.posNodes, self.negNodes) = (self.jsonData['positive_nodes'], self.jsonData['negative_nodes'])
            self.hotWordUsers.update({hWord: (self.posNodes, self.negNodes)})
        dbc.execute("SELECT word FROM  newterm WHERE freq BETWEEN %f AND %f", self.lTh, self.hTh)
        self.candidWords = cur.fetchall()
        for cWord in self.candidWords:
            dbc.execute("SELECT user FROM tweets WHERE id IN (SELECT id FROM tweets_newterm WHERE word = %s)", cWord)
            self.newwordUsers = cur.fetchall()
            (self.posNodes, self.negNodes) = self.hotwordUsers[cWord]
            posIntersect = set(self.newwordUsers).intersection(set(self.posNodes))
            negIntersect = set(self.newWordUsers).intersection(set(self.negNodes))
            
            
    
    def recommendTweets(self):
        
        
        
