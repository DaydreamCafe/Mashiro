# -*- coding:utf-8 -*-
"""
插件线程
"""
import threading
import func_timeout


def run_command(command, client, logger):
    def command_thread():
        @func_timeout.func_set_timeout(command['max_time'])
        def _run_command():
            command['target_func'](client)

        try:
            _run_command()
        except func_timeout.exceptions.FunctionTimedOut:
            logger.warning('[WatchDog]Killed processing command {}'.format(args[0]))

    thread = threading.Thread(target=command_thread)
    thread.setDaemon(True)
    thread.start()
