# -*- coding:utf-8 -*-
"""
通道类型
"""
import time

from mashiro.constants import core_constants


class ChannelFullException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self, *args, **kwargs):
        return self.error


class Channel:
    """
    通道类型
    """
    def __init__(self, length_limit: int = 128) -> None:
        # 设置最大长度
        self.length_limit = length_limit
        self._channel = list()

    def __lshift__(self, other) -> None:
        """向Channel中添加元素"""
        if len(self._channel) < self.length_limit or self.length_limit == -1:
            self._channel.append(other)
        else:
            raise ChannelFullException('The limit({}) of channel elements has been reached and cannot continue adding '
                                       'elements to it'.format(self.length_limit))

    def pop(self):
        element = self._channel[0]
        del self._channel[0]
        return element

    def __getitem__(self, item):
        return self._channel.__getitem__(item)

    def __len__(self) -> int:
        return self._channel.__len__()

    def __repr__(self):
        return self._channel.__repr__()
