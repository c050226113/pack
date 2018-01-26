import threading
import time

from util.lib.Util import Util
from util.mysql.Connection import Connection


class txz_task:
    def initDbConfig(self):
        if self.debug:
            self._201 = {
                'host': '192.168.0.201',
                'user': 'txz',
                'pwd': 'txz1234',
            }
            self._204 = {
                'host': '192.168.0.204',
                'user': 'txz',
                'pwd': 'txz1234',
            }
        else:
            self._201 = {
                'host': 'rds73834du7837gios3drw.mysql.rds.aliyuncs.com',
                'user': 'roottxz',
                'pwd': 'roottxz',
            }
            self._204 = {
                'host': 'rds3i3854c247386ne9o.mysql.rds.aliyuncs.com',
                'user': 'roottxz',
                'pwd': 'roottxz',
            }

    def __init__(self, **kwargs):
        self.debug = Util.get_key('debug', kwargs, Util.is_test())

        self._201 = {}
        self._204 = {}
        self.config = {
            'txz_audio_qqmusic': 204,
            'TXZ_AUDIO_DATA': 201,
            'txz_audio_leTing': 204,
            'TXZ_AUDIO': 201,
            'txz_audio_sort': 204,
            'txz_audio_himalaya': 204,
            'txz_audio_kaola': 204,
            'txz_audio_history': 204
        }
        self.connections = {}

        self.initDbConfig()

    def getDbConnection(self, dbName):
        if dbName not in self.connections:
            if dbName not in self.config:
                print('no db config')
                exit()
            host = self.config[dbName]
            if host == 201:
                conf = self._201
            elif host == 204:
                conf = self._204
            else:
                conf = {}
                print('has no connection config')
                exit()

            self.connections[dbName] = Connection(conf['host'], conf['user'], conf['pwd'], dbName)

        return self.connections[dbName]


class t_task:
    def __init__(self, **kwargs):
        self.max_thread_num = Util.get_key('max_thread_num', kwargs, 1)
        self.no_use_thread = [i for i in range(self.max_thread_num)]

    def thread_wait_for_can_start(self):
        while 1:
            if len(self.no_use_thread) > 0:
                return self.no_use_thread.pop()
            else:
                time.sleep(0.5)

    def add_task(self, thread_callback, _tuple):
        threadName = self.thread_wait_for_can_start()
        thread = thread_task(threadName, self, thread_callback, _tuple)
        thread.start()

    def wait_task(self):
        count = 0
        while 1:
            if len(self.no_use_thread) != self.max_thread_num:
                print(self.no_use_thread)
                count += 1
                time.sleep(1)
                if count > 100:
                    break
                else:
                    continue
            else:
                break


class thread_task(threading.Thread):
    def __init__(self, threadName, parent: t_task, callback, _tuple):
        super().__init__(name=str(threadName))
        self.threadIndex = threadName
        self.parent = parent
        self.tuple = _tuple
        self.callback = callback

    def run(self):
        self.callback(self, *self.tuple)
        self.parent.no_use_thread.append(self.threadIndex)
