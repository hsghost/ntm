# -*- coding: utf-8 -*-
"""
Module ntm.db.dbo

New Terms Miner Databases Operations Module

@author: Aifeng Yun

    This module is for generating the database operational commands required 
    to manipulate the databases. The dba and dbi modules calls for procedures 
    in this module to generate the desired dommands before sending them to
    execute on the servers.

"""

from .. import _NTM_
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

class dboMeta(_NTM_):
    """
        The dbo metaclass templates classes for generating 
        operational commands used for manipulate different 
        types of databases.
    """

class dboFactory(object):
    """
        Factory class for all dynamically generated 
        dbo classes.
    """
    __metaclass__ = dboMeta