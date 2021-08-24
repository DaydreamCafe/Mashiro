# -*- coding:utf-8 -*-
"""
日志模块
"""
import datetime
import os

import yaml

from colorama import init, Fore


class Logger:
    """日志器"""

    def __init__(self, location):
        # 获取日志等级
        with open('./config/MashiroConfig.yaml', 'r', encoding='utf8') as f:
            __config = yaml.load(f, Loader=yaml.FullLoader)
        self.log_level = __config['DebugConfig']['LogLevel']
        self.__level = {
            'DEBUG': 4,
            'INFO': 3,
            'NOTICE': 2,
            'WARNING': 1,
            'ERROR': 0,
        }
        self.__color_config = {
            'DEBUG': Fore.BLUE,
            'INFO': Fore.GREEN,
            'NOTICE': Fore.LIGHTYELLOW_EX,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
        }
        self.location = location

        # 初始化Colorama
        init(autoreset=True)

        # 初始化日志文件
        # self.log_path = './logs'
        # if not os.path.exists(self.log_path):
        #     os.mkdir(self.log_path)
        # with open(os.path.join(self.log_path, ))

    def debug(self, msg):
        if self.__level[self.log_level] > 3:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(
                '[{}]{}[DEBUG]{}[{}]{}'.format(now_time, self.__color_config['DEBUG'], Fore.WHITE, self.location, msg))

    def info(self, msg):
        if self.__level[self.log_level] > 2:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('[{}]{}[INFO]{}[{}]{}'
                  .format(now_time, self.__color_config['INFO'], Fore.WHITE, self.location, msg))

    def notice(self, msg):
        if self.__level[self.log_level] > 1:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('[{}]{}[NOTICE]{}[{}]{}'
                  .format(now_time, self.__color_config['NOTICE'], Fore.WHITE, self.location, msg))

    def warning(self, msg):
        if self.__level[self.log_level] > 0:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('[{}]{}[WARNING]{}[{}]{}'
                  .format(now_time, self.__color_config['WARNING'], Fore.WHITE, self.location, msg))

    def error(self, msg):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('[{}]{}[ERROR]{}[{}]{}'.format(now_time, self.__color_config['ERROR'], Fore.WHITE, self.location, msg))
