# -*- coding: utf-8 -*-
"""
Module ntm.logs.logs

New Terms Miner Logging Utility

@author: Aifeng Yun

    This module is impelented to facilitate the logging operations 
    required by the New Terms Miner.

"""

import logging, logging.handlers, logging.config
import pickle
import SocketServer
import struct
import time

running = False

class NtmLogsLoggerAdapter(logging.LoggerAdapter):
    """
    """
    pass

class NtmLogsFilter(logging.Filter):
    """
    """
    pass

class NtmLogsContextualFilter(logging.Filter):
    """
        This class provides custom logging filter functionality 
        along with contextual information injection.
    """
    pass

class NtmLogsFormatter(logging.Formatter):
    """
        This class provides custom logging formatter functionality
        such as UTC time and single-line recording.
    """

    def __init__(self, fmt = None, datefmt = None, utc = False, single_line = True):
        if utc:
            self.converter = time.gmtime
        self.singleline = single_line
        return super(NtmLogsFormatter, self).__init__(fmt, datefmt)
    
    def formatException(self, ei):
        """
            Format exceptions to accomodate single-line event logging.
        """
        if not self.singleline:
            return super(NtmLogsFormatter, self).formatException(ei)
        else:
            return repr(super(NtmLogsFormatter, self).formatException(ei))

    def format(self, record):
        fmtstr = super(NtmLogsFormatter, self).format(record)
        if self.singleline and record.exc_text:
            fmtstr = fmtstr.replace('\n', ' ')
        return fmtstr

class NtmLogsNullHandler(logging.NullHandler):
    """
    """
    pass

class NtmLogsSocketHandler(logging.handlers.SocketHandler):
    """
    """
    pass

class NtmLogsFilesHandler(logging.handlers.RotatingFileHandler):
    """
        This class provides 
    """
    pass

class NtmLogsConsoleHandler(logging.StreamHandler):
    pass

class NtmLogsStreamRequestHandler(SocketServer.StreamRequestHandler):
    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        logger.handle(record)

    def handle(self):
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

class NtmLogsSocketReciver(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

    serviceconfig = {
        "host": 'localhost',
        "port": logging.handlers.DEFAULT_TCP_LOGGING_PORT, 
        "handler": NtmLogsStreamRequestHandler
        }

    def __init__(self, config):
        self.serviceconfig.update(config)
        super(NtmLogsSocketReciver, self).__init__((self.serviceconfig["host"], self.serviceconfig["port"]), self.serviceconfig["handler"])
        self.abort = False
        self.timeout = True
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = False
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

def run(config):
    running = True
    logsservice = NtmLogsSocketReciver(config["service"])
    logsservice.serve_until_stopped()
