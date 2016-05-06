# -*- coding: utf-8 -*-
__all__ = [ 'db', ]

from .. import _NTM_
from .. import dictConfig
from .. import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from .. import jsonOp
from dba import dbaMeta

#with jsonOp() as j:
#    with j.Read("config.json", "config.schema") as config:
#        dictConfig(config["logging"])
