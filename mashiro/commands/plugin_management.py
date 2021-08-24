# -*- coding:utf-8 -*-
"""插件管理相关"""
import json

from mashiro.api.interface import Interface
from mashiro.utils.plugin_manager import MashiroPlugin
from mashiro.utils.logger import Logger

# 初始化Logger
logger = Logger('plugin_management.py')

# 被禁用的指令列表
disabled_command_list = list()

# 初始化命令
with open('./data/plugins/disabled_plugin.json', 'r', encoding='utf8') as f:
    # 被禁用的插件列表
    disabled_plugin_list = json.loads(f.read())
# 插件列表
plugin = MashiroPlugin()
plugin_list = plugin.read_plugin_list()


def disable(client: Interface):
    """禁用插件或指令"""

    # 禁用插件
    if client.args[1] == 'plugin' and client.get_permission(client.raw_msg['user_id']):
        existence = False
        # 寻找插件对应索引
        for i in range(0, len(plugin_list)):
            if client.plugin_list[i]['plugin_name'] == client.args[2]:
                # 从已安装插件列表中删除
                del plugin_list[i]
                # 重写已安装插件列表
                plugin.write_plugin_list(plugin_list)
                # 重写禁用列表
                with open('./data/plugins/disabled_plugin.json', 'w', encoding='utf8') as f:
                    # 被禁用的插件列表
                    f.write(json.dumps(disabled_plugin_list))
                # 回显
                reply = {
                    "action": "send_group_msg",
                    "params": {
                        "group_id": client.react_group,
                        "message": "已禁用插件:{}".format(client.args[2])
                    }
                }
                client.send(reply)
                logger.info('Disabled plugin {}'.format(client.args[2]))
        if not existence:
            reply = {
                "action": "send_group_msg",
                "params": {
                    "group_id": client.react_group,
                    "message": "未找到插件:{}".format(client.args[2])
                }
            }
            client.send(reply)
            logger.warning('Failed to disable plugin {}, because the plugin was not loaded'.format(client.args[2]))

    # TODO: 禁用指令


def enable(client: Interface):
    """启用插件或指令"""
    # TODO: 启用指令或插件
    pass
