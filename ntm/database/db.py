# -*- coding: utf-8 -*-
"""
Module ntm.database.db

New Terms Miner Databases Module

@author: Aifeng Yun

    This module is impelented to facilitate the acess, management and 
    initialization to the databases required by the New Terms Miner.

"""

from .. import _NTM_
from .. import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from uuid import uuid1

class dboMeta(_NTM_):
    """
        The dbo metaclass templates classes for generating 
        operational commands used for manipulate different 
        types of databases.
    """
    pass

class dboFactory(object):
    """
        Factory class for all dynamically generated 
        dbo classes.
    """
    __metaclass__ = dboMeta
    factory_class = True

class dbaMeta(_NTM_):
    """
        The dba metaclass templates classes for accessing
        different database platforms.
    """

    def __call__(self, obj_cfg = dict(), dbo = None, *args):
        #   Move this to __init__ in the config file
        if not ('dba_type' in obj_cfg and dbo):
            self.log(ERROR, "Failed loading dba configuration. Database access initialization aborted.")
            return (None)
        elif obj_cfg['dba_type'] == "mysql":
            try:
                self.config = {
                    'host': obj_cfg['dbs_addr'],
                    'port': obj_cfg['dbs_port'],
                    'user': obj_cfg['dbs_login'],
                    'password': obj_cfg['dbs_pass'],
                    'use_unicode': obj_cfg['dbs_unicode'],
                    'charset': obj_cfg['dbs_charset'],
                    'time_zone': '%+03d:00' % ((time.timezone if (time.localtime().tm_isdst == 0) else time.altzone) / -3600),
                    'max_recursive_level': obj_cfg['dbs_max_recursive_level']
                    }
            except KeyError as kye:
                self.log(ERROR, "Invalid database configuration.")
                return None
            except ValueError as vle:
                self.log(ERROR, "Invalid database configuration.")
                return (None)
            else:
                self.dbo = dbo # (extra, config['dbs_operations'])
                try:
                    self.config['database'] = obj_cfg['dbs_default_db']
                except KeyError as kye:
                    self.log(WARNING, "No database specified, connecting to the server only.")
                    pass
                try:
                    MySQLConnection.__init__(**self.config)
                    #return super(dba, self).__init__(config)
                except mysqlc.Error as dce:
                    self.log(ERROR, "Connot connect to the database server specified.")
        return super(dbaMeta, self).__call__(obj_cfg, *args)

class dbaFactory(object):
    """
        Factory class for all dynamically generated 
        dba classes.
    """
    __metaclass__ = dbaMeta
    factory_class = True

class dbiMeta(_NTM_):
    """ 
        The dbi metaclass templates classes for initializing 
        different types of databases.
    """

    #   Move this to the config file
    #def __init__(self, config, *args, **kwargs):
    #    self.dbsConfig = config['dbs']
    #    self.dbConfig = config['db']
    #    self.dbAccess = dba(self.dbsConfig)
    #    if not all((self.dbsConfig, self.dbConfig, self.dbAccess)):
    #        return (None)
    #    else:
    #        return super(dbi, self).__init__(*args, **kwargs)

    #   Move this to the config file
    #def initDB(self, **kwargs):
    #    if not self.createDB():
    #        self.log(ERROR, "Failed creating database. Aborting the dbi process...")
    #        return (False)
    #    if not self.createBanks(self.dbConfig['db_banks']):
    #        self.log(ERROR, "Failed to create data banks.")
    #        return (False)
    #    else:
    #        self.log(INFO, "Data banks creation succeded.")
    #        return (True)

class dbiFactory(object):
    __metaclass__ = dbiMeta
    factory_class = True
