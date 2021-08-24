# -*- coding:utf-8 -*-
"""
发送消息的消息栈
"""
import json
import threading
import time

from mashiro.utils.config import MashiroConfig
from mashiro.utils.logger import Logger


class MessageStack:
    """发送消息的消息栈，防止机器人发送速度过快被封"""
    def __init__(self, sender):
        # 初始化Logger
        self.logger = Logger('message_stack.py')

        _config = MashiroConfig().read()
        # 初始化栈深度
        self.stack_depth = _config['MashiroConfig']['SendingStackDepth']
        # 初始化发送间隔
        self.interval = _config['MashiroConfig']['SendingInterval']
        # 初始化栈
        self.stack = list()
        # 发送器方法，来自于websocket提供的send()方法
        self.send = sender

        # 启动msg stack
        self.__run()

    def add(self, msg: dict):
        """向信息栈添加信息"""
        self.logger.debug('Added msg "{}" to msg stack'.format(msg))
        if self.stack_depth == 0 or len(self.stack) <= self.stack_depth:
            self.stack.append(msg)
        else:
            self.logger.notice('Message stack overflowed!Ignored message adding request.')

    def __run(self):
        """开始处理消息栈"""
        def send_msg():
            """在一个新线程里跑"""
            while True:
                if self.stack:
                    self.send(json.dumps(self.stack[len(self.stack) - 1]))

                    # 草泥马忘加这两行代码了，debug的时候往群里灌了4000+消息
                    del self.stack[len(self.stack) - 1]
                time.sleep(self.interval)

        thread = threading.Thread(target=send_msg)
        thread.setDaemon(True)
        thread.start()
