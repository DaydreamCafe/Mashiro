# -*- coding:utf-8 -*-
import logging
import pkgutil

from mashiro.utils.config import MashiroConfig


class Parser:
    """没什么卵用的解析器类，但是不能删"""
    def __init__(self):
        pass


class ParserLoader:
    def __init__(self):
        # 默认自定义解析器位置
        self.custom_parser_path = './mashiro/parsers/custom'

        # 加载配置文件
        _config = MashiroConfig().read()
        self.parser_name = _config['ParseConfig']['Parser']
        self.command_identifier = _config['CommandConfig']['CommandIdentifier']

    def load(self) -> Parser:
        """加载解析器，返回一个解析器对象"""
        parser = Parser()

        logging.info('Start loading parser...')
        if self.parser_name == 'BuiltIn':
            # 加载内建解析器
            logging.info('Selected parser: Built-In parser')
            from mashiro.parsers import builtin_parser
            parser = builtin_parser.Parser(command_identifier=self.command_identifier)
        else:
            # 加载外部解析器
            logging.info('Trying to load external parser: {}'.format(self.parser_name))
            for finder, name, ispck in pkgutil.walk_packages([self.custom_parser_path]):
                if name == self.parser_name:
                    loader = finder.find_module(name)
                    parser = loader.load_module(name).Parser(self.command_identifier)
                    logging.info('Loaded parser {}'.format(self.parser_name))
                else:
                    # 在没有可用的外部解析器的情况下加载内建解析器
                    logging.warning('Parser {} not found, switched to Built-In parser'.format(self.parser_name))
                    from mashiro.parsers import builtin_parser
                    parser = builtin_parser.Parser(command_identifier=self.command_identifier)

        return parser
