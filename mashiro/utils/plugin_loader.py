# -*- coding:utf-8 -*-
"""
插件加载器
"""
import json
import os
import pkgutil

from mashiro.utils.config import MashiroConfig
from mashiro.utils.plugin_manager import MashiroPlugin
from mashiro.utils.logger import Logger


class PluginLoader:
    """插件加载器"""

    def __init__(self):
        self.logger = Logger('plugin_loader.py')

        _config = MashiroConfig().read()
        self.plugin_path = _config['PluginConfig']['PluginPath']
        self.default_max_time = _config['CommandConfig']['MaxResponseTime']
        self.plugin_list_path = './data/plugins/installed_plugin.json'

    def load(self):
        """加载函数方法"""
        # 插件列表
        plugin_list = list()
        # cqhttp客户端启动时调用的插件函数
        on_start_func = list()
        # 特定指令调起的插件函数
        on_message_func = list()
        # 任意消息调起的插件函数
        on_message_func_no_prefix = list()

        # 获取已安装的插件列表
        installed_plugin_list = MashiroPlugin().read_plugin_list()

        # 遍历列表加载插件
        for plugin in installed_plugin_list:
            plugin_path = os.path.join(self.plugin_path, plugin['plugin_id'])

            for finder, name, ispck in pkgutil.walk_packages([plugin_path]):
                # 加载插件
                with open(os.path.join(plugin_path, 'metadata.json')) as f:
                    metadata = json.loads(f.read())
                if name == metadata['main_module'][2:-3]:
                    self.logger.info('Loading plugin: {}'.format(plugin['plugin_name']))
                    loader = finder.find_module(name)
                    plugin_ = loader.load_module(name)
                    self.logger.info('Loaded plugin: {}'.format(plugin['plugin_name']))

                    # 初始化插件
                    try:
                        plugin_.init_plugin()
                        self.logger.info('Initialized plugin: {}'.format(plugin['plugin_name']))
                    except NameError:
                        self.logger.info('No initialization function found in plugin: {}, skipped'
                                         .format(plugin['plugin_name']))

                    # 注册插件
                    self.logger.info('Registering plugin {}'.format(metadata['plugin_id']))
                    try:
                        commands_list = [command['command'] for command in plugin_.command_register]
                    except AttributeError:
                        commands_list = []
                    plugin_list.append({
                        'metadata': metadata,
                        'commands': commands_list,
                    })

                    # 注册on_start函数
                    try:
                        on_start_func.append({
                            'plugin_id': metadata['plugin_id'],
                            'target_func': plugin_.on_start,
                        })
                        self.logger.info('Registering on start func(PluginID:{})'.format(metadata['plugin_id']))
                    except AttributeError:
                        pass

                    # 注册指令
                    try:
                        if plugin_.command_register:
                            self.logger.info('Registering on message func(PluginID:{})'.format(metadata['plugin_id']))
                            for command in plugin_.command_register:
                                # 注册钩子指令
                                if command['type'] == 'trigger':
                                    if not ('max_time' in command.keys()):
                                        command['max_time'] = self.default_max_time
                                    on_message_func.append(command)
                                # 注册主动指令
                                elif command['type'] == 'active':
                                    if not ('max_time' in command.keys()):
                                        command['max_time'] = self.default_max_time
                                    on_message_func_no_prefix.append(command)
                    except AttributeError:
                        pass

        return plugin_list, on_start_func, on_message_func, on_message_func_no_prefix
