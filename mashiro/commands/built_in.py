# -*- coding:utf-8 -*-
"""内建指令集"""
from mashiro.commands import plugin_management

registered_command = {
    'enable': plugin_management.enable,
    'disable': plugin_management.disable,
    }
