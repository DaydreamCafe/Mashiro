# -*- coding:utf-8 -*-
import pkgutil

from mashiro.utils.config import MashiroConfig
from mashiro.utils.logger import Logger


class Parser:
    """用于编码提示的、没什么卵用的解析器类，但是不能删"""
    def __init__(self):
        pass

    def parse(self, data):
        pass


class ParserLoader:
    def __init__(self):
        # 初始化logger
        self.logger = Logger('parser_loader.py')

        # 默认自定义解析器位置
        self.custom_parser_path = './mashiro/parsers/custom'

        # 加载配置文件
        _config = MashiroConfig().read()
        self.parser_name = _config['ParseConfig']['Parser']
        self.command_identifier = _config['CommandConfig']['CommandIdentifier']

    def load(self) -> Parser:
        """加载解析器，返回一个解析器对象"""
        parser = Parser()

        self.logger.info('Start loading parser...')
        if self.parser_name == 'BuiltIn':
            # 加载内建解析器
            self.logger.info('Selected parser: Built-In parser')
            from mashiro.parsers import builtin_parser
            parser = builtin_parser.Parser(command_identifier=self.command_identifier)
        else:
            # 加载外部解析器
            self.logger.info('Trying to load external parser: {}'.format(self.parser_name))
            for finder, name, ispck in pkgutil.walk_packages([self.custom_parser_path]):
                if name == self.parser_name:
                    loader = finder.find_module(name)
                    parser = loader.load_module(name).Parser(self.command_identifier)
                    self.logger.info('Loaded parser {}'.format(self.parser_name))
                else:
                    # 在没有可用的外部解析器的情况下加载内建解析器
                    self.logger.warning('Parser {} not found, switched to Built-In parser'.format(self.parser_name))
                    from mashiro.parsers import builtin_parser
                    parser = builtin_parser.Parser(command_identifier=self.command_identifier)

        return parser
