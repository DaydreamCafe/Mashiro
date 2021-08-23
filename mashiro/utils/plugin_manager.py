# -*- coding:utf-8 -*-
"""
管理插件的类
"""
import json
import logging
import os
import shutil
import zipfile

from mashiro.utils.config import MashiroConfig


class MashiroPlugin:
    """
    用来对.Mashiro格式的插件进行管理的类
    """

    def __init__(self):
        _config = MashiroConfig().read()
        self.plugin_path = _config['PluginConfig']['PluginPath']
        self.plugin_temp_path = './temp'
        self.plugin_list_path = './data/plugins/installed_plugin.json'

    def read_plugin_list(self) -> list:
        """读取已安装插件的列表"""
        with open(self.plugin_list_path, 'r', encoding='utf8') as f:
            plugin_list = json.loads(f.read())
            return plugin_list

    def write_plugin_list(self, plugin_metadata: list):
        """写入插件列表"""
        with open(self.plugin_list_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(plugin_metadata))

    def install(self, plugin_name):
        """安装插件"""
        path = os.path.join(self.plugin_path, plugin_name) + '.Mashiro'
        logging.info('Now installing plugin {}'.format(plugin_name))

        # 解压插件到临时文件夹
        if os.path.exists(self.plugin_temp_path):
            # 若临时文件夹已存在则先删除
            shutil.rmtree(self.plugin_temp_path)
        os.mkdir(self.plugin_temp_path)
        with zipfile.ZipFile(path, 'r') as plugin:
            plugin.extractall(os.path.join(self.plugin_temp_path, plugin_name))

        # 检查插件安装状态
        with open(os.path.join(self.plugin_temp_path, plugin_name, 'metadata.json')) as f:
            metadata = json.loads(f.read())
            plugin_metadata = {
                'plugin_id': metadata['plugin_id'],
                'plugin_name': metadata['plugin_name'],
            }
        installed_plugin_list = self.read_plugin_list()
        if plugin_metadata not in installed_plugin_list:
            # 安装
            installation_path = os.path.join(self.plugin_path, plugin_metadata['plugin_id'])
            if not os.path.exists(installation_path):
                # 如果目标路径不存在原文件夹的话就创建
                os.makedirs(installation_path)
            if os.path.exists(installation_path):
                # 如果目标路径存在原文件夹的话就先删除
                shutil.rmtree(installation_path)
            shutil.copytree(os.path.join(self.plugin_temp_path, plugin_name), installation_path)

            # 安装配置文件
            config_path = metadata['config_path']
            if config_path != '':
                shutil.copytree(os.path.join(installation_path, config_path.replace('./', '', 1)),
                                os.path.join('./config', plugin_metadata['plugin_id']))
                shutil.rmtree(os.path.join(installation_path, config_path.replace('./', '', 1)))

            # 添加到已安装列表
            installed_plugin_list.append(plugin_metadata)
            self.write_plugin_list(installed_plugin_list)

            logging.info('Successfully installed plugin: {}(ID:{})'.format(plugin_name, plugin_metadata['plugin_id']))
        else:
            # 已安装时跳过安装
            logging.info('Already installed plugin {}(ID:{}),skipped the installation'
                         .format(plugin_name, plugin_metadata['plugin_id']))

        # 清理
        shutil.rmtree(self.plugin_temp_path)

    def install_all(self):
        """安装所有插件"""
        # 遍历插件文件夹
        plugin_list = os.listdir(self.plugin_path)

        # 去除列表中的文件夹
        for file in plugin_list:
            if not file.endswith('.Mashiro'):
                del plugin_list[plugin_list.index(file)]

        # 安装
        for i in range(0, len(plugin_list)):
            print(plugin_list)
            print(plugin_list[i][0:-8])
            self.install(plugin_list[i][0:-8])

    def uninstall(self, plugin_name):
        """卸载插件"""
        installed_plugin_list = self.read_plugin_list()
        # 遍历已安装插件列表，获取插件id
        existence = False
        if installed_plugin_list:
            for plugin in installed_plugin_list:
                if plugin['plugin_name'] == plugin_name:
                    # 删除插件
                    shutil.rmtree(os.path.join(self.plugin_path, plugin['plugin_id']))

                    # 删除配置文件
                    shutil.rmtree(os.path.join('./config', plugin['plugin_id']))

                    # 从插件列表移除
                    del installed_plugin_list[installed_plugin_list.index(plugin)]
                    self.write_plugin_list(installed_plugin_list)
                    existence = True
            if not existence:
                logging.warning('Plugin {} is not installed,skipped uninstallation'.format(plugin_name))
        else:
            logging.warning('No installed plugin')

    def uninstall_all(self):
        """卸载所有插件"""
        installed_plugin_list = self.read_plugin_list()
        # 遍历已安装插件列表，获取插件id
        if installed_plugin_list:
            for plugin in installed_plugin_list:
                # 删除插件
                shutil.rmtree(os.path.join(self.plugin_path, plugin['plugin_id']))

                # 删除配置文件
                shutil.rmtree(os.path.join('./config', plugin['plugin_id']))

            # 从插件列表移除
            self.write_plugin_list([])
        else:
            logging.warning('No installed plugin')

    def reinstall(self, plugin_name):
        """重新安装插件"""
        self.uninstall(plugin_name)
        self.install(plugin_name)
        logging.info('Reinstalled plugin {}'.format(plugin_name))

    def reinstall_all(self):
        """重新安装所有插件"""
        self.uninstall_all()
        self.install_all()
        logging.info('Reinstalled all plugins')
