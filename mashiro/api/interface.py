# -*- coding:utf-8 -*-
"""
插件交互接口
"""
from mashiro.utils.config import PermissionConfig


class Interface:
    """一个用于插件与Mashiro交互的类"""
    def __init__(self, react_group: int, add_msg, plugin_list, on_message_func, load_plugin, close, raw_msg: dict = None,
                 args: list = None):
        # 目标群号
        self.react_group = react_group
        # 向消息栈添加消息
        self.add = add_msg
        # 插件列表
        self.plugin_list = plugin_list
        # 钩子指令列表
        self.on_message_func = on_message_func
        # 加载插件
        self.load_plugin = load_plugin
        # 关闭Websocket连接
        self.close = close
        # Parser解析的原始消息
        self.raw_msg = raw_msg
        # Parser解析的指令
        self.args = args

    def send(self, msg: dict):
        """发送信息"""
        self.add(msg)

    def set_args__(self, args):
        """设置解析的命令"""
        self.args = args

    def set_raw_msg__(self, raw_msg):
        """设置原始信息"""
        self.raw_msg = raw_msg

    @staticmethod
    def get_permission(uid: int):
        """获取用户权限等级"""
        permission_config = PermissionConfig().read()
        if uid in permission_config['Owner']:
            return 0
        elif uid in permission_config['Admin']:
            return 1
        elif uid in permission_config['Member']:
            return 2
        else:
            return -1
