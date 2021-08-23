# -*- coding:utf-8 -*-
import logging
import sys
import threading

from mashiro.clients.cqhttp_client import CqHttpClient
from mashiro.utils.config import MashiroConfig


class Mashiro:
    @staticmethod
    def run():
        """启动go-cqhttps的守护进程"""

        # 启动client线程
        def _run_client():

            _config = MashiroConfig().read()
            client = CqHttpClient(_config['MashiroConfig']['ReactGroup'], _config['cqhttpConfig']['IpAddress'],
                                  _config['cqhttpConfig']['Port'], _config['cqhttpConfig']['Token'])
            client.run()

        thread = threading.Thread(target=_run_client)
        thread.setDaemon(True)
        thread.start()

        # 捕捉Ctrl+C
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logging.info('Programme is exiting...')
            sys.exit(1)
