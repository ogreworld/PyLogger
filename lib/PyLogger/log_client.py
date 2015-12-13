#!usr/bin/python
# -*- coding: utf-8 -*-
#
# file_name: log_client
# description: 
# author: libo
# Histort:
# 	first created: 2015/11/6

import socket
import logging
import logging.handlers
from logging.handlers import SocketHandler

import log_settings


def getLogger(name, level=logging.DEBUG):
    logger = logging.Logger(name)
    socket_handler = SocketHandler('localhost', log_settings.Instance.PORT)
    datefmt = "%Y-%m-%d %H:%M:%S"
    format_str = "[%(asctime)s]: %(levelname)s - %(message)s"
    formatter = logging.Formatter(format_str, datefmt)
    socket_handler.setFormatter(formatter)
    socket_handler.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)

    logger.addHandler(socket_handler)
    logger.addHandler(stream_handler)

    return logger

def is_server_started():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("localhost", log_settings.PORT))
        client.close()
        return True
    except:
        print "Server not started"
        return False

def set_logging_to_file(file_path):
    tmp_logger = getLogger(log_settings.LOGGER_NAME_CHANGE_PATH)
    tmp_logger.info(file_path)

def enable_logging_to_file():
    tmp_logger = getLogger(log_settings.LOGGER_NAME_SAVE_IN_FILE_TRUE)
    tmp_logger.info("Enable logging to file")

def disable_logging_to_file():
    tmp_logger = getLogger(log_settings.LOGGER_NAME_SAVE_IN_FILE_FALSE)
    tmp_logger.info("Disable logging to file")

def set_log_server_port(port):
    i = log_settings.Instance()
    i.__class__.PORT = int(port)
