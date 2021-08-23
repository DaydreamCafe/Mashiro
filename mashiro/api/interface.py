# -*- coding:utf-8 -*-
"""
插件交互接口
"""


class Interface:
    """一个用于插件与Mashiro交互的类"""
    def __init__(self, react_group: int):
        self.react_group = react_group

    def send(self, msg: dict):
        pass
