# -*- coding:utf-8 -*-
"""
一个配置文件类
用于对配置文件的操作
"""
import sys
import yaml

from mashiro.utils.logger import Logger


class __Config:
    """配置文件的抽象类"""
    def __init__(self):
        # 初始化logger
        self.logger = Logger('config.py')
        self.config_path = ''

    def read(self) -> dict:
        """加载配置文件，返回配置文件字典"""
        self.logger.debug('Trying to load config file: {}'.format(self.config_path))
        try:
            with open(self.config_path, 'r', encoding='utf8') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)

        except FileNotFoundError:
            self.logger.error('Config file {} does not exists'.format(self.config_path))
            sys.exit(1)

        self.logger.debug('Loaded config file: {}'.format(self.config_path))
        return config


class MashiroConfig(__Config):
    """用于操作Mashiro基础设置的类"""
    def __init__(self):
        super(MashiroConfig, self).__init__()
        self.config_path = './config/MashiroConfig.yaml'


class PermissionConfig(__Config):
    """用于操作Mashiro权限配置的类"""
    def __init__(self):
        super(PermissionConfig, self).__init__()
        self.config_path = './config/PermissionConfig.yaml'
