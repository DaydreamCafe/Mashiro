# -*- coding:utf-8 -*-
"""
cqhttp的客户端
"""
import logging
import sys
import threading

import func_timeout
import websocket

from mashiro.utils.parser_loader import ParserLoader
from mashiro.utils.plugin_loader import PluginLoader
from mashiro.utils.plugin_manager import MashiroPlugin
from mashiro.api.interface import Interface
from mashiro.utils.message_stack import MessageStack
from mashiro.commands import built_in
from mashiro.utils.config import MashiroConfig


class CqHttpClient(websocket.WebSocketApp):
    def __init__(self, react_group_id: int, ip: str, port: int, token: str):
        # Websocket基本设置
        self.ws_address = ip
        self.ws_port = port
        self.access_token = token
        self.react_group_id = react_group_id
        self.client_to_query_stats = '1'
        self.client_to_query_online = '2'
        websocket.enableTrace(True)
        url = f'ws://{self.ws_address}:{self.ws_port}/'
        if self.access_token != '':
            url += '?access_token={}'.format(self.access_token)

        # 连接至Websocket服务器
        logging.info('Now connecting to {}'.format(url))
        super().__init__(url, on_message=self.on_message)

        # 加载字符串解析器
        logging.info('Parser loading phase')
        self.parser = ParserLoader().load()

        # 安装插件
        logging.info('Plugin installing phase')
        MashiroPlugin().install_all()

        # 加载插件
        logging.info('Plugin loading phase')
        self.plugin_list, self.on_start_func, self.on_trigger_command, self.on_active_command = PluginLoader().load()

        # 初始化消息栈
        self.msg_stack = MessageStack(self.send)

        # 初始化统一插件接口
        self.client = Interface(react_group=self.react_group_id, add_msg=self.msg_stack.add, close=exit,
                                on_message_func=self.on_active_command, plugin_list=self.plugin_list,
                                load_plugin=self.load_plugins)

    def load_plugins(self):
        # 加载插件
        logging.info('Plugin loading phase')
        self.plugin_list, self.on_start_func, self.on_trigger_command, self.on_active_command = PluginLoader().load()

    def run(self):
        def on_start_thread(*args):
            """插件on_start函数线程启动函数"""
            args[0](args[1])

        # 启动on_start函数线程
        for on_start_func in self.on_start_func:
            thread = threading.Thread(target=on_start_thread, args=(on_start_func, self.client))
            thread.setDaemon(True)
            thread.start()

        # 启动go-cqhttp连接
        self.run_forever()

    def on_message(self, data):
        """消息调起的函数"""
        try:
            # 解析原始数据
            raw_msg, args = self.parser.parse(data)
            # 初始化专用插件接口
            client = Interface(react_group=self.react_group_id, add_msg=self.msg_stack.add, close=exit,
                               on_message_func=self.on_active_command, plugin_list=self.plugin_list,
                               load_plugin=self.load_plugins, args=args, raw_msg=raw_msg)
            # 设置通用接口
            self.client.set_args__(args)
            self.client.set_raw_msg__(raw_msg)

            # 调用内置指令
            if args[0] in built_in.registered_command.keys():
                @func_timeout.func_set_timeout(MashiroConfig().read()['CommandConfig']['CommandIdentifier'])
                def run_command():
                    built_in.registered_command[args[0]](client)

                try:
                    run_command()
                except func_timeout.exceptions.FunctionTimedOut:
                    logging.warning('[WatchDog]Killed processing command {}'.format(args[0]))

            # 调用钩子指令
            for command in self.on_trigger_command:
                if command['command'] == args[0]:
                    @func_timeout.func_set_timeout(command['max_time'])
                    def run_command():
                        command['target_func'](client)

                    try:
                        run_command()
                    except func_timeout.exceptions.FunctionTimedOut:
                        logging.warning('[WatchDog]Killed processing command {}'.format(args[0]))

            # 调用主动式指令
            for command in self.on_active_command:
                def command_thread():
                    @func_timeout.func_set_timeout(command['max_time'])
                    def _run_command():
                        command['target_func'](client)

                    try:
                        _run_command()
                    except func_timeout.exceptions.FunctionTimedOut:
                        logging.warning('[WatchDog]Killed processing command {}'.format(args[0]))

                thread = threading.Thread(target=command_thread)
                thread.setDaemon(True)
                thread.start()

        except TypeError:
            # 尚不明确错误原因
            pass

    def exit(self):
        """结束Websocket Client"""
        self.close()
        logging.info('Closed connection.Exiting client...')
        sys.exit(0)
