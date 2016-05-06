# -*- coding: utf-8 -*-
"""
Module ntm.db.dba

New Terms Miner Databases Access Module

@author: Aifeng Yun

    This module is impelented to facilitate the acess to the databases 
    required by the New Terms Miner.

"""

from .. import _NTM_
from .. import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from uuid import uuid1


class dbaMeta(_NTM_):
    """
        The dba metaclass templates classes for accessing
        different database platforms.
    """

    def useDB(self, **kwargs):
        pass

    def insertRecords(self, inserts, **kwargs):
        pass

    def deleteRecords(self, deletes, **kwargs):
        pass

    def updateRecords(self, updates, **kwargs):
        pass

    def queryRecords(self, query, **kwargs):
        pass

    def __call__(self, obj_cfg = dict(), dbo = None, *args):
        # Move this to __init__ in the config file
        #if not ('dba_type' in obj_cfg and dbo):
        #    self.log(ERROR, "Failed loading dba configuration. Database access initialization aborted.")
        #    return (None)
        #elif obj_cfg['dba_type'] == "mysql":
        #    try:
        #        self.config = {
        #            'host': obj_cfg['dbs_addr'],
        #            'port': obj_cfg['dbs_port'],
        #            'user': obj_cfg['dbs_login'],
        #            'password': obj_cfg['dbs_pass'],
        #            'use_unicode': obj_cfg['dbs_unicode'],
        #            'charset': obj_cfg['dbs_charset'],
        #            'time_zone': '%+03d:00' % ((time.timezone if (time.localtime().tm_isdst == 0) else time.altzone) / -3600),
        #            'max_recursive_level': obj_cfg['dbs_max_recursive_level']
        #            }
        #    except KeyError as kye:
        #        self.log(ERROR, "Invalid database configuration.")
        #        return None
        #    except ValueError as vle:
        #        self.log(ERROR, "Invalid database configuration.")
        #        return (None)
        #    else:
        #        self.dbo = dbo # (extra, config['dbs_operations'])
        #        try:
        #            self.config['database'] = obj_cfg['dbs_default_db']
        #        except KeyError as kye:
        #            self.log(WARNING, "No database specified, connecting to the server only.")
        #            pass
        #        try:
        #            MySQLConnection.__init__(**self.config)
        #            #return super(dba, self).__init__(config)
        #        except mysqlc.Error as dce:
        #            self.log(ERROR, "Connot connect to the database server specified.")
        return super(dbaMeta, self).__call__(obj_cfg, *args)

class dbaFactory(object):
    """
        Factory class for all dynamically generated 
        dba classes.
    """
    __metaclass__ = dbaMeta
    factory_class = True
