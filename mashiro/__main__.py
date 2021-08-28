# -*- coding:utf-8 -*-
import os

from mashiro.utils.logger import Logger
from mashiro.clients.cqhttp_client import CqHttpClient
from mashiro.utils.config import MashiroConfig


class Mashiro:
    logger = Logger('__main__.py')
    logger.info('Mashiro is running(PID: {})'.format(os.getpid()))

    @staticmethod
    def run():
        """启动go-cqhttps的进程"""
        _config = MashiroConfig().read()
        client = CqHttpClient(_config['MashiroConfig']['ReactGroup'], _config['cqhttpConfig']['IpAddress'],
                              _config['cqhttpConfig']['Port'], _config['cqhttpConfig']['Token'])
        client.run()
