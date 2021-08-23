# -*- coding:utf-8 -*-

def is_command(identifier: list, msg: str):
    for prefix in identifier:
        if msg.startswith(prefix):
            return True, prefix
    return False, None
