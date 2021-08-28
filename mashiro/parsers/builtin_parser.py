# -*- coding:utf-8 -*-
"""
内建解析器
"""
from mashiro.api import parser_api


class Parser:
    def __init__(self, command_identifier: list):
        self.command_identifier = command_identifier

    @staticmethod
    def format(data: dict):
        """重新格式化cqhttp传回的json"""
        if data['anonymous'] is None:
            is_anonymous = False
        else:
            is_anonymous = True
        return {
            'is_anonymous': is_anonymous,
            'font': data['font'],
            'group_id': data['group_id'],
            'post_type': data['post_type'],
            'self_id': data['self_id'],
            'anonymous': data['anonymous'],
            'message': {
                'type': data['message_type'],
                'id': data['message_id'],
                'message_seq': data['message_seq'],
                'content': data['message'],
                'raw_content': data['raw_message'],
            },
            'sender': data['sender'],
            'sub_type': data['sub_type'],
            'time': data['time'],
            'user_id': data['user_id'],
        }

    def parse(self, data: dict):
        """解析方法"""
        identifier = parser_api.is_command(self.command_identifier, data['raw_message'])
        # 解析带有命令前缀的命令
        if identifier[0]:
            args = data['raw_message'].replace(identifier[1], '', 1).split(' ')
        else:
            args = [data['raw_message']]
        return self.format(data), args
