# -*- coding:utf-8 -*-
"""
cqhttp的客户端
"""
import logging

import websocket

from mashiro.utils.parser_loader import ParserLoader


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
        self.parser = ParserLoader().load()
