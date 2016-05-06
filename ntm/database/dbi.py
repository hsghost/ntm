# -*- coding: utf-8 -*-
"""
Module ntm.db.dbi

New Terms Miner Database Initialization Module

@author: Aifeng Yun

    This module is impelented to facilitate the initialization
    process of the database required by the New Terms Miner.

"""

from .. import _NTM_
from .. import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from ntm.db.dba import dba

class dbiMeta(_NTM_):
    """ 
        The dbi metaclass templates classes for initializing 
        different types of databases.
    """

    #   Move this to config file
    #def __init__(self, config, *args, **kwargs):
    #    self.dbsConfig = config['dbs']
    #    self.dbConfig = config['db']
    #    self.dbAccess = dba(self.dbsConfig)
    #    if not all((self.dbsConfig, self.dbConfig, self.dbAccess)):
    #        return (None)
    #    else:
    #        return super(dbi, self).__init__(*args, **kwargs)

    def createDB(self, **kwargs):
        pass

    def deleteDB(self, database, **kwargs):
        pass

    def createBanks(self, tbs_config, **kwargs):
        pass

    def deleteBanks(self, tables, **kwargs):
        pass

    def initDB(self, **kwargs):
        if not self.createDB():
            self.log(ERROR, "Failed creating database. Aborting the dbi process...")
            return (False)
        if not self.createBanks(self.dbConfig['db_banks']):
            self.log(ERROR, "Failed to create data banks.")
            return (False)
        else:
            self.log(INFO, "Data banks creation succeded.")
            return (True)
