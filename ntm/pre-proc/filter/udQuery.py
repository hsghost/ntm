# -*- coding: utf-8 -*-
"""
Module udQuery
Version 1.2

CIS 700 M004 - Social Media Mining
Fall 2014 Term Project

Last modified Dec 14, 2014

@author: Aifeng Yun

    This module is intended to handle the query to Urban Dictionay though its 
    API.
    
"""

from urllib import quote as urlquote
from urllib2 import urlopen
import json

class udQuery:
    url = ""
    jsonFile = None
    jsonData = None
    
    def recorded(self, term):
        self.url = "http://api.urbandictionary.com/v0/define?term=%s" % \
            urlquote(term)
        
        try:
            self.jsonFile = urlopen(self.url)
            self.jsonData = json.loads(self.jsonFile.read().decode('utf-8'))
        except Exception:
            return True
        
        if self.jsonData['result_type'] == u'exact' or \
            self.jsonData['result_type'] == u'fulltext':
            return True
        else:
            return False
    
        
    