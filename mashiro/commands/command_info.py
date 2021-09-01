# -*- coding:utf-8 -*-
"""info指令"""
from mashiro.api.interface import Interface

info_msg = """
[CQ:image,file=https://pic.imgdb.cn/item/612f9e4c44eaada73960ba70.png]
Mashiro——基于go-cqhttp由Python实现的QQ机器人
-----------------------------------------
版本: Alpha-0.0.3 Unstable-Nightly-Build
内部版本号: Build-21090100063
更新日志请查阅Github项目Release说明
-----------------------------------------
Github项目地址:
https://github.com/BotMashiro
使用说明&开发文档:
https://botmashiro.github.io/MashiroDocs
欢迎Star以支持，也欢迎高质量的代码提交和BUG反馈
请注意, 开发者并没有义务回复您的问题. 您应该具备
基本的提问技巧.
有关如何提问，请阅读《提问的智慧》.
-----------------------------------------
基于本软件进行的使用、修改、二次分发等行为，请遵
守 GNU General Public License v3.0 协议.
详细信息请访问: 
http://www.gnu.org/licenses/gpl-3.0.html
-----------------------------------------
本项目使用的图标由@WhitePaper233授权使用，未经
允许，不得用于其他用途.
https://github.com/WhitePaper233
"""


def command_info(client: Interface):
    msg = {
        'action': 'send_group_msg',
        'params': {
            'group_id': client.react_group,
            'message': info_msg,
        },
    }
    client.send(msg)
