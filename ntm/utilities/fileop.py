# -*- coding: utf-8 -*-
"""
Module ntm.utilities.fileop

New Terms Miner File Operation Utility

@author: Aifeng Yun

    This module is impelented to facilitate the file operations 
    required by the New Terms Miner.

"""

from .. import _NTM_
from .. import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
import os, io, json, errno
import jsonschema as jsm
from copy import deepcopy

running = False

class fileOp(_NTM_):
    """ This clas ...   """
    fd = None
    f = None

    def __init__(self, *args, **kwargs):
        return super(fileOp, self).__init__(*args, **kwargs)

class jsonOp(_NTM_):
    """
        This class provides convinent access handlers for 
        accessing local JSON files
    """

    jsonFD = None
    jsonFile = None
    jsonData = None
    jsonSmFile = None
    jsonSchema = None

    def __init__(self, *args, **kwargs):
        return super(jsonOp, self).__init__(*args, **kwargs)

    def Read(self, filePath = "", schemaPath = ""):
        if schemaPath:
            try:
                self.jsonSmFile = io.open(schemaPath, mode = 'r')
                self.jsonSchema = json.loads(self.jsonSmFile.read().decode('utf-8'))
            except IOError as ioe:
                self.log(ERROR, "Error reading schema file.")
                return None
            except ValueError as vle:
                self.log(ERROR, "Error resolving schema file.")
                return None
        try:
            self.jsonFile = io.open(filePath, mode = 'r')
            self.jsonData = json.loads(self.jsonFile.read().decode('utf-8'))
        except IOError as ioe:
            self.log(ERROR, "Error reading JSON file.")
            return None
        except ValueError as vle:
            self.log(ERROR, "Error resolving JSON file.")
            return None
        if schemaPath:
            try:
                jsm.validate(self.jsonData, self.jsonSchema, format_checker = jsm.FormatChecker(), )
            except jsm.SchemaError as sme:
                self.log(ERROR, "Error validating schema file.")
                return None
            except jsm.FormatError as fme:
                self.log(ERROR, "Error validating value format. The given JSON file is invalid and cannot be loaded.")
                return None
            except jsm.ValidationError as vle:
                self.log(ERROR, "The given JSON file is invalid and cannot be loaded.")
                return None
        return (deepcopy(self.jsonData))

    def Write(self, filePath = "", fileData = None, shcemaPath = "", overwrite = False):
        if shcemaPath:
            try:
                self.jsonSmFile = io.open(shcemaPath, mode = 'r')
                self.jsonSchema = json.loads(self.jsonSmFile.read().decode('utf-8'))
                jsm.validate(fileData, self.jsonSchema, format_checker = jsm.FormatChecker())
            except IOError as ioe:
                self.log(ERROR, "Error reading schema file.")
                return False
            except ValueError as vle:
                self.log(ERROR, "Error resolving schema file.")
                return False
            except jsm.SchemaError as sme:
                print ("Error validating schema file.\n\t%s" % sme)
                self.log(ERROR, "Error validating schema file.")
                return False
            except jsm.FormatError as fme:
                self.log(ERROR, "Error validating value format. The given JSON data is invalid and cannot be exported.")
                return False
            except jsm.ValidationError as vle:
                self.log(ERROR, "The given JSON data is invalid and cannot be exported.")
                return False
        try:
            self.jsonFD = os.open(filePath, os.O_CREAT | 0x0 if overwrite else os.O_EXCL | os.O_WRONLY)
        except OSError as ose:
            if ose.errno == errno.EEXIST:
                self.log(ERROR, "Error writing to JSON file: file already existed.")
                return False
            else:
                raise
        else:
            try:
                self.jsonFile = os.fdopen(self.jsonFD, mdoe = 'w', encoding = 'utf-8')
                self.jsonFile.write(unicode(json.dumps(fileData, ensure_ascii=False)))
            except IOError as ioe:
                self.log(ERROR, "Error wirting data to file.\n\t%s")
            else:
                return True
