#!usr/bin/python
# -*- coding: utf-8 -*-
#
# file_name: log_server
# description: log server for all logging template
# author: libo
# Histort:
# 	first created: 2015/11/6

# standard lib
import os
import datetime
import logging
import traceback
import struct
import cPickle                 # use cPickle for speed

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

# from twisted.internet import epollreactor
#
# epollreactor.install()

# local lib
import log_settings
from log_record import initlog

class ReceiveProtocol(Protocol):

    HEADER_LENGTH = 4
    LOG_FILE_PATH = "default.log"
    SAVE_IN_FILE = False

    def __init__(self):
        self.buf = ''
        self.state = 'init'
        self.require_length = ReceiveProtocol.HEADER_LENGTH
        # 记录当前完成初始化的logger名称
        self.logger_dict = {}
        # self.logger = logging.getLogger("LogServer")
        # self.log_file_path = gen_log_file_path(log_file_path)
        # self.logger = initlog("LogServer", self.__gen_log_server_file_path(), logging.DEBUG)

    def __get_log_server_path(self):
        curr_path = os.path.realpath(__file__)
        curr_dir = os.path.split(curr_path)[0]
        log_path = os.path.join(os.path.split(curr_dir)[0], "log")
        return log_path


    def __gen_log_server_file_path(self):
        curr_date = datetime.datetime.now()
        curr_file_name = "-".join([str(curr_date.year), str(curr_date.month), str(curr_date.day)])
        curr_dir = self.__get_log_server_path()
        return os.path.join(curr_dir, curr_file_name)

    def connectionMade(self):
        # self.logger.info(u'[makeConnection]与logger_client建立socket连接。')
        pass

    def dataReceived(self, data):
        try:
            if len(self.buf + data) >= self.require_length:
                self.buf = self.buf + data
                # 数据就绪进行相应动作
                data = self.buf[0:self.require_length]
                # 把数据从缓冲区中取走
                self.buf = self.buf[self.require_length:]
                self.solve(data)
                # 可能一次读到了多条日志记录
                if self.buf:
                    self.dataReceived('')
            else:
                self.buf += data

        except BaseException, e:
            print u"读取日志失败:" + str(e) + '\n' + traceback.format_exc()

    def solve(self, data):
        statehandler = None
        try:
            pto = 'proto_' + self.state
            statehandler = getattr(self,pto)
        except AttributeError:
            self.logger.error('callback',self.state,'not found')
            self.transport.loseConnection()

        statehandler(data)
        if self.state == 'done':
            self.transport.loseConnection()

    def connectionLost(self, reason):
        # self.logger.info(u'[connectionLost]与logger_client的socket连接关闭。')
        pass

    def set_log_file_path(self, path):
        self.__class__.LOG_FILE_PATH = path

    def set_save_in_file_status(self, status):
        self.__class__.SAVE_IN_FILE = status

    # 记录日志
    def proto_record(self, data):
        logRecord = logging.makeLogRecord(cPickle.loads(data))

        if logRecord.name in log_settings.LOGGER_NAME_LIST:
            if logRecord.name == log_settings.LOGGER_NAME_CHANGE_PATH:
                self.set_log_file_path(logRecord.getMessage())
            elif logRecord.name == log_settings.LOGGER_NAME_SAVE_IN_FILE_TRUE:
                self.set_save_in_file_status(True)
            elif logRecord.name == log_settings.LOGGER_NAME_SAVE_IN_FILE_FALSE:
                self.set_save_in_file_status(False)
        else:
            if (logRecord.name, self.LOG_FILE_PATH) not in self.logger_dict:
                logger = initlog(logRecord.name, self.LOG_FILE_PATH, log_level=logging.DEBUG, save_in_file=self.SAVE_IN_FILE)
                self.logger_dict.update({(logRecord.name, self.LOG_FILE_PATH):logger})

            self.logger_dict[(logRecord.name, self.LOG_FILE_PATH)].handle(logRecord)

            # 修改下一步动作以及所需长度
            self.state = 'init'
            self.require_length = ReceiveProtocol.HEADER_LENGTH

    # 处理头部信息
    def proto_init(self, data):
        length = struct.unpack('!I', data[0:ReceiveProtocol.HEADER_LENGTH])[0]

        # 修改下一步动作以及所需长度
        self.state = 'record'
        self.require_length = length

        if len(self.buf) >= self.require_length:
            data = self.buf[0:self.require_length]
            # 把数据从缓冲区中取走
            self.buf = self.buf[self.require_length:]
            self.solve(data)


class ReceiveFactory(Factory):

    def buildProtocol(self, addr):
        return ReceiveProtocol()

class LogServer(object):
    def __init__(self):
        pass

    # def set_log_path(self, path):
    #     set_log_file_path(path)

    def run_server(self, port):
        # if port is None:
        #     port = log_settings.Instance.PORT
        print "Starting Log Server..."
        print "Listening on port:%s"%port
        reactor.listenTCP(port, ReceiveFactory())
        reactor.run()
        print "Log server has stoped..."

    def stop_server(self):
        reactor.stop()

def main():
    # print 'logserver has started.'
    # logger = logging.getLogger('LogServer')
    # logger.info('logserver has started.')
    #
    # reactor = twisted.internet.reactor
    # reactor.listenTCP(log_settings.PORT, ReceiveFactory())
    # reactor.run()
    log_server = LogServer()
    log_server.run_server(log_settings.Instance.PORT)

if __name__ == '__main__':
    main()