__all__ = [ 'fileop' ]

from .. import _NTM_
from .. import dictConfig
from .. import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from fileop import jsonOp

#with jsonOp() as j:
#    with j.Read("config.json", "config.schema") as config:
#        dictConfig(config["logging"])
