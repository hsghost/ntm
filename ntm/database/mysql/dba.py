# -*- coding: utf-8 -*-
"""
Module ntm.db.mysql.dba

New Terms Miner Database Access Implementation for MySQL

@author: Aifeng Yun

    This module is impelented to facilitate the acess to the MySQL 
    database required by the New Terms Miner.

"""

from .. import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from ntm.db.dba import dba
from ntm.db.mysql.dbo import dbo
from mysql.connector.connection import MySQLConnection
import mysql.connector as mysqlc
from mysql.connector import errorcode
import time
from string import strip



class dbaMySQL(dba, MySQLConnection):
    """ This dba class provides MySQL database access facilities   """

    def __init__(self, obj_cfg = dict(), dbo = None, *args, **kwargs):
        if not obj_cfg:
            self.log(ERROR, "Failed loading dba configuration. Database access initialization aborted.")
            return (None)
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
            self.dbo = dbo
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
                return (None)

    def useDB(self, **kwargs):
        try:
            self.database = dict(self.dbConfig).update(kwargs)['database']
        except mysqlc.Error as dce:
            self.log(ERROR, "Connot use the database with the name specified.")
            return (False)
        else:
            return (True)

    def executeDML(self, DML, **kwargs):
        if not self.cursor():
            self.log(ERROR, "Error accessing database connection. DML execution aborted.")
            return (False)
        for item in DML:
            try:
                self.cursor().execute(DML)
            except mysqlc.Error as ede:
                self.log(ERROR, ede.message)
                return (False)
        return (True)

    def executeDQL(self, DQL, **kwargs):
        if not self.cursor():
            self.log(ERROR, "Error accessing database connection. DQL execution aborted.")
            return (False)
        try:
            self.cursor().execute(DQL)
        except mysqlc.Error as eqe:
            self.log(ERROR, eqe.message)
            return (False)
        return (True)

    def insertRecords(self, inserts, **kwargs):
        if not inserts:
            self.log(ERROR, "Failed to resolve parameters. Data insertion aborted.")
            return (False)
        if 'select_expr' in inserts[0]:
            DML = self.dbo.dmlInsertSelect(inserts, recursive_level_reset = True)
        else:
            DML = self.dbo.dmlInsert(inserts, recursive_level_reset = True)
        if not DML:
            self.log(ERROR, "Failed to generate DML. Data insertion aborted.")
            return (False)
        return (self.executeDML(DML))

    def deleteRecords(self, deletes, **kwargs):
        if not tables:
            self.log(ERROR, "Failed to resolve parameters. Data deletion aborted.")
            return (False)
        DML = self.dbo.dmlDelete(deletes, recursive_level_reset = True)
        if not DML:
            self.log(ERROR, "Failed to generate DML. Data deletion aborted.")
            return (False)
        return (self.executeDML(DML))

    def updateRecords(self, updates, **kwargs):
        if not updates:
            self.log(ERROR, "Failed to resolve parameters. Data update aborted.")
            return (False)
        DML = self.dbo.dmlUpdate(updates, recursive_level_reset = True)
        if not DML:
            self.log(ERROR, "Failed to generate DML. Data update aborted.")
        return (self.executeDML(DML))

    def queryRecord(self, query, **kwargs):
        if not (query and 'select' in query):
            self.log(ERROR, "Failed to resolve parameters. Data query aborted.")
            return (False)
        DQL = self.dbo.dqlSelect(query['select'], recursive_level_reset = True)
        if not DQL:
            self.log(ERROR, "Failed to generate DQL. Data query aborted.")
        return (self.executeDQL(DQL))
