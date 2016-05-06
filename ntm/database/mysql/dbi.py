# -*- coding: utf-8 -*-
"""
Module ntm.db.mysql.dbi

New Terms Miner Database Initialization Module

@author: Aifeng Yun

    This module is impelented to facilitate the initialization
    process of the database required by the New Terms Miner.

"""

from ntm.ntm import _NTM_
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
import mysql.connector as mysqlc
from mysql.connector import errorcode
from ntm.db.dba import dba

class dbi(_NTM_):
    """ The dbi class provides database initialization routines """

    dbsConfig = None
    dbConfig = None
    dbAccess = None
    dbCursor = None
    TABLES = { }

    def __init__(self, obj_cfg, *args, **kwargs):
        self.dbsConfig = obj_cfg['dbs']
        self.dbConfig = obj_cfg['db']
        self.dbAccess = dba(self.dbsConfig)
        if not all((self.dbsConfig, self.dbConfig, self.dbAccess)):
            return None
        else:
            self.dbCursor = self.dbAccess.cursor()
            return super(dbi, self).__init__(*args, **kwargs)

    def ddlCreateDB(self, **kwargs):
        obj_cfg = dict(self.dbsConfig).update(**kwargs)
        DDL = {
            'create_database_' + obj_cfg['db_name']: "CREATE DATABASE {db_name} {charset}".format(
            db_name = obj_cfg['db_name'],
            charset = "DEFAULT CHARACTER SET " + obj_cfg['dbs_charset'] 
            ),
            }
        return DDL

    def ddlDropDB(self, database, if_exists = False):
        if not database:
            self.log(WARNING, "Failed generating DROP DATABASE DDL: No database specified.")
            return None
        DDL = {
            'disable_foreign_key_checks': "SET FOREIGN_KEY_CHECKS = 0",
            'drop_database_' + database: "DROP DATABASE {existance} {db_name}".format(
            existance = "IF EXISTS" if if_exists else "",
            db_name = database
            ),
            'dependency_order': [ database ],
            }
        return DDL

    def ddlCreateTables(self, tbs_config, **kwargs):
        if not tbs_config:
            self.log(ERROR, "Error generating CREATE TABLES DDL: Invalid tbs_config.")
            return None
        if not self.dbAccess.database:
            self.log(ERROR, "Error generating CREATE TABLES DDL: No target database specified.")
            return None
        DDL = { }
        UIN = REF_COL = COL = LINES = TABLE = [ ]
        REF = ""
        for table_name in tbs_config['dependency_order']:
            table_def = tbs_config[table_name]
            for column_name in table_def['columns']['dependency_order']:
                column_def =table_def['columns'][column_name]
                LINES.append("\t`{name}` {type}({length}{decimals}{elements}) {unsigned} {zerofill} {nullability} {default} {auto_increment} {column_format} {storage}".format(
                    name = column_name,
                    type = column_def['data_type'],
                    length = str(column_def['data_length']) if 'data_length' in column_def else "",
                    decimals = (", " + str(column_def['data_decimals'])) if 'data_decimals' in column_def else "",
                    elements = (", ".join(column_def['elements'])) if 'elements' in column_def else "",
                    unsigned = "UNSIGNED" if ('unsigned' in column_def and column_def['unsigned'] == True) else "",
                    zerofill = "ZEROFILL" if ('zerofill' in column_def and column_def['zerofill'] == True) else "",
                    nullability = ("NULL" if column_def['nullable'] else "NOT NULL") if 'nullable' in column_def else "",
                    default = ("DEFAULT " + column_def['default']) if 'default' in column_def else "",
                    auto_increment = "AUTO INCREMENT" if ('auto_increment' in column_def and column_def['auto_increment'] == True) else "",
                    comment = "COMMENT " + column_def['comment'] if 'comment' in column_def else "",
                    column_format = ("COLUMN_FORMAT " + column_def['column_format']) if 'column_format' in column_def else "",
                    sotrage = ("STORAGE " + column_def['sotrage']) if 'storage' in column_def else ""
                    ))
            if 'indexes' in table_def:
                for index_name in table_def['indexes']['dependency_order']:
                    index_def = table_def['indexes'][index_name]
                    for index_col_name in index_def['index_columns']['dependency_order']:
                        index_col_def = index_def['index_columns'][index_col_name]
                        COL.append("`{name}` {order}".format(
                            name = index_col_name,
                            order = index_col_def
                            ))
                    if 'references' in index_def:
                        for ref_col_name in index_def['references']['ref_columns']['dependency_order']:
                            ref_col_def = index_def['references']['ref_columns'][ref_col_name]
                            REF_COL.append("`{name}` {order}".format(
                                name = ref_col_name,
                                order = ref_col_def
                                ))
                        REF = "REFERENCES `{ref_table}` {ref_columns} {matching} {delete} {update}".format(
                            ref_table = index_def['references']['ref_table'],
                            ref_columns = ", ".join(REF_COL),
                            matcching = index_def['references']['matching'],
                            delete = index_def['references']['on_delete'],
                            update = index_def['references']['on_update']
                            )
                    LINES.append("\t{constraint_symbol} {index_command} `{name}` ({index_columns}) {references}".format(
                        constraint_symbol = ("CONSTRAINT `" + index_def['constraint_symbol'] + "`") if 'constraint_symbol' in index_def else "",
                        index_command = index_def['index_command'],
                        name = index_def['index_name'] if 'index_name' in index_def else "",
                        index_columns = ", ".join(COL),
                        references = REF
                        ))
            if 'check' in table_def:
                LINES.append("\tCHECK {check}".format(
                    check = table_def['check']
                    ))
            if 'row_format' in table_def:
                LINES.append("\tROW_FORMAT {row_format}".format(
                    row_format = table_def['row_format']
                    ))
            if 'union' in table_def:
                UNI = ['`' + u + '`' for u in table_def['union']]
                LINES.append("\tUNION ({union_tables})".format(
                    union_tables = ", ".join(UNI)
                    ))
            if 'select_clause' in table_def:
                LINES.append(table_def['select_clause'])
            TABLE = (
                "CREATE {temporary} TABLE {if_not_exist} `{name}` (".format(
                    temporary = "TEMPORARY" if ('temporary' in table_def and table_def['temporary'] == True) else "",
                    if_not_exist = "IF NOT EXIST" if ('use_existing' in table_def and table_def['use_existing'] == True) else "",
                    name = table_name
                   ) + 
                ", ".join(LINES) + 
                "){engine}".format(
                    engine = (" ENGINE " + table_def['engine']) if 'engine' in table_def else ""
                    )
                )
            DDL['create_table_' + table_name] = TABLE
        DDL['dependency_order'] = tbs_config['dependency_order']
        return DDL

    def ddlDropTables(self, tables, temporary = False, if_exists = False):
        if not tables:
            self.log(WARNING, "Failed generating DROP TABLES DDL: Empty tables list specified.")
            return None
        DDL = {
            'drop_tables': "DROP {temp} TABLE {table_list} {existance}".format(
                temp = "TEMPORARY" if temporary else "",
                table_list = ", ".join(tables),
                existance = "IF EXISTS" if if_exists else ""
                )
            }
        return DDL

    def executeDDL(self, DDL, **kwargs):
        for item_name in DDL['dependency_order']:
            item_ddl = DDL[item_name]
            try:
                self.log(INFO, "Executing DDL: {operation}...".format(
                    operation = item_name,
                    )
                            )
                self.dbCursor.execute(item_ddl)
            except mysqlc.Error as ede:
                self.log(ERROR, ede.message)
                return False
        return True

    def createDB(self, **kwargs):
        try:
            self.executeDDL(ddlCreateDB(**kwargs))
        except Exception as e:
            self.log(ERROR, e.message)
            return False
        else:
            return True

    def deleteDB(self, database, **kwargs):
        try:
            self.executeDDL(ddlDropDB(**kwargs))
        except Exception as e:
            self.log(ERROR, e.message)
            return False
        else:
            return True

    def initDB(self, **kwargs):
        if not self.createDB():
            self.log(ERROR, "Failed creating database. Aborting the initialization process...")
            return False
        else:
            try:
                self.dbAccess.database = self.dbsConfig['db_name']
            except KeyError as kye:
                self.log(ERROR, "Invalid database configuration.")
                return False
            except mysqlc.Error as dbe:
                if dbe.errno == errorcode.ER_BAD_DB_ERROR:
                    self.log(ERROR, dbe.message)
                return False
            else:
                if not self.createBanks(self.dbConfig['db_tables']):
                    self.log(ERROR, "Failed to create tables.")
                    return False
                else:
                    self.log(INFO, "Database tables creation succeded.")
                    return True

    def createBanks(self, **kwargs):
        pass

    def deleteBanks(self, **kwargs):
        pass

