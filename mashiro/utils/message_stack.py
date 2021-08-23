# -*- coding:utf-8 -*-
"""
发送消息的消息栈
"""
import json
import threading

from mashiro.utils.config import MashiroConfig


class MessageStack:
    """发送消息的消息栈，防止机器人发送速度过快被封"""
    def __init__(self, sender):
        _config = MashiroConfig().read()
        # 初始化栈深度
        self.stack_depth = _config['SendingStackDepth']
        # 初始化发送间隔
        self.interval = 1
        # 初始化栈
        self.stack = list()
        # 发送器方法，来自于websocket提供的send()方法
        self.send = sender

    def add(self, msg: dict):
        """向信息栈添加信息"""
        if self.stack_depth == 0 or len(self.stack) <= self.stack_depth:
            self.stack.append(msg)

    def __run(self):
        """开始处理消息栈"""
        def send_msg():
            """在一个新线程里跑"""
            while True:
                self.send(json.dumps(self.stack[len(self.stack) - 1]))

        thread = threading.Thread(target=send_msg)
        thread.setDaemon(True)
        thread.start()
