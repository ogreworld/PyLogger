#!usr/bin/python
# -*- coding: utf-8 -*-
#
# file_name: log_record
# description: 
# author: libo
# Histort:
# 	first created: 2015/11/9

__author__ = 'libo'

import ctypes
import logging
# from logging.handlers import TimedRotatingFileHandler

def initlog(logger_name, log_file_path, log_level=logging.DEBUG, save_in_file=True):
    logger = logging.Logger(logger_name)
    #
    # for handler in logger.handlers:
    #     logger.removeHandler(handler)

    datefmt = "%Y-%m-%d %H:%M:%S"
    format_str = "[%(asctime)s]: %(levelname)s - %(name)s - %(message)s"
    formatter = logging.Formatter(format_str, datefmt)

    #  file handler
    if save_in_file:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

    try:
        stream_handler = ColorizingStreamHandler()
    except:
        stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    # stream_handler.emit = decorate_emit(stream_handler.emit)

    logger.addHandler(stream_handler)
    logger.setLevel(log_level)

    return logger

class ColorizingStreamHandler(logging.StreamHandler):

    FOREGROUND_RED = 0x0c
    FOREGROUND_GREEN = 0x02
    FOREGROUND_WHITE = 0x0f
    FOREGROUND_YELLOW = 0x0e
    FOREGROUND_BLUE = 0x09

    FOREGROUND_DARKWHITE = 0x07
    FOREGROUND_DARKRED = 0x04
    FOREGROUND_DARKSKYBLUE = 0x03
    FOREGROUND_DARKGREEN = 0x02
    FOREGROUND_DARKGRAY = 0x08


    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE= -11
    STD_ERROR_HANDLE = -12

    def __init__(self, *args, **kwargs):
        self._colors = {logging.DEBUG: self.FOREGROUND_WHITE,
                        logging.INFO: self.FOREGROUND_GREEN,
                        logging.WARNING: self.FOREGROUND_YELLOW,
                        logging.ERROR: self.FOREGROUND_RED,
                        }
        super(ColorizingStreamHandler, self).__init__(*args, **kwargs)
        self.std_out_handler = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        self.std_err_handler = ctypes.windll.kernel32.GetStdHandle(self.STD_ERROR_HANDLE)

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def emit(self, record):
        try:
            message = self.format(record)
            stream = self.stream
            if not self.is_tty:
                stream.write(message)
            else:
                self.__set_test_color(self._colors[record.levelno])
                # message = self._colors[record.levelno] + message + self.RESET
                stream.write(message)
                self.__reset_tex_color()
            stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def setLevelColor(self, logging_level, escaped_ansi_code):
        self._colors[logging_level] = escaped_ansi_code

    def __set_test_color(self, color):
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.std_out_handler, color)
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.std_err_handler, color)

    def __reset_tex_color(self):
        self.__set_test_color(self.FOREGROUND_DARKWHITE)

def decorate_emit(fn):
    # add methods we need to the class
    def new(*args):
        levelno = args[0].levelno
        if(levelno >= logging.CRITICAL):
            color = '\x1b[31;1m'
        elif(levelno >= logging.ERROR):
            color = '\x1b[31;1m'
        elif(levelno >= logging.WARNING):
            color = '\x1b[33;1m'
        elif(levelno >= logging.INFO):
            color = '\x1b[32;1m'
        elif(levelno >= logging.DEBUG):
            color = '\x1b[35;1m'
        else:
            color = '\x1b[0m'
        # add colored *** in the beginning of the message
        args[0].msg = "{0}***\x1b[0m {1}".format(color, args[0].msg)

        # new feature i like: bolder each args of message
        args[0].args = tuple('\x1b[1m' + arg + '\x1b[0m' for arg in args[0].args)
        return fn(*args)
    return new