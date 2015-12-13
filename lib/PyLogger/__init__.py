#!usr/bin/python
# -*- coding: utf-8 -*-
#
# file_name: __init__.py
# description: 
# author: libo
# Histort:
# 	first created: 2015/11/12
#####################################################
# Examples:
# > import PyLogger
# > logger = PyLogger.getLogger("test")
# > logger.debug("hahahaha")
#


__author__ = 'libo'
__version__ = "1.0"

from log_server import LogServer
from log_client import *
from log_settings import *



def start_server(port=None):
    if port is None:
        port = Instance.PORT
    log_server = LogServer()
    log_server.run_server(port)

if __name__ == '__main__':
    start_server()