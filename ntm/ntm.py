# -*- coding: utf-8 -*-
from logging import getLogger, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from logs.logs import NtmLogsLoggerAdapter
from sys import exc_info
from types import DictType
from uuid import uuid1

class _NTM_(type):
    """
        The ancestor of all ntm metaclasses and metaclass 
        of all ntm classes to provide universal facilities 
        such as logging and subclass creation.
    """

    locale = DictType()
    extra = DictType()
    methods = DictType()
    functions = DictType()

    def _strToBase(cls, str):
        try:
            return (tuple(set(eval(str))))
        except SyntaxError as ste:
            cls.log(ERROR, ste.message)
            raise

    def _checkCodeSecurity(cls, source):
        pass    #   Exception sould be raised if risk is detected.

    def log(cls, loglevel = INFO, logmsg = str(), exc = None, *args, **kwargs):
        if exc is None:
            exc = exc_info()
        message = cls.locale[logmsg] if logmsg in cls.locale else logmsg
        cls.adapter.log(loglevel, message, exc, *args, **kwargs)

    def addFunctions(cls, funcs):
        try:
            for func_name, func_code in funcs:
                exec(func_code, cls.__dict__)
        except SyntaxError as ste:
            cls.log(ERROR, ste.message)
            return False
        except TypeError as tpe:
            cls.log(ERROR, tpe.message)
            return False
        else:
            return True

    def createClass(fcty, cls_dict = DictType()):
        if not ('cls_sig' in cls_dict and 'cls_bases' in cls_dict):
            cls.log(ERROR, "Invalid cls_dict configuration.")
            return None
        cls_name_ = fcty.__name__.rsplit("Factory")[0] + "_" + cls_dict['cls_sig']
        try:
            new_cls = fcty.__metaclass__(
                name = cls_name_ + "_" + uuid1().get_hex() if 'use_uuid' in cls_dict and cls_dict['use_uuid'] else "", 
                bases = fcty._strToBase(cls_dict['cls_bases']).append(fcty), 
                dict = cls_dict
                )
        except Exception as nce:
            cls.log(ERROR, nce.message)
            return None
        else:
            if hasattr(fcty.__metaclass__, 'methods') and cls_name_ in fcty.__metaclass__.methods:
                succ = new_cls.addFunctions(fcty.__metaclass__.methods[cls_name_])
            return (new_cls)

    def __new__(meta, name = str(), bases = tuple(), dict = DictType()):
        if ('methods' in dict) and (not name in meta.methods):
            meta.methods[name] = { }
            try:
                for func_name, func_source in dict['methods']:
                    meta._checkCodeSecurity(func_source)
                    meta.methods[name][func_name] = compile(func_source, '<string>', 'exec')
            except SyntaxError as ste:
                meta.log(ERROR, ste.message)
                raise
            except TypeError as tpe:
                meta.log(ERROR, tpe.message)
                raise
        return super(_NTM_, meta).__new__(name, bases, dict)

    def __init__(cls, name = str(), bases = tuple(), dict = DictType(), *args, **kwargs):
        if not ('factory_class' in dict and dict['factory_class']):
            # classCreator disabled for common operational classes
            delattr(cls, "classCreator")
        logger = getLogger(name = __name__)
        cls.adapter = NtmLogsLoggerAdapter(logger, cls.extra)
        return super(_NTM_, self).__init__(name, bases, dict)

    def __call__(self, obj_cfg = dict(), *args):
        self.log = _NTM_.log
        self.config = obj_cfg
        return super(_NTM_, self).__call__(*args)

class NTM(object):
    """
        Ancestor class for all NTM operational classes.
    """

    __metaclass__ = _NTM_
    factory_class = False
