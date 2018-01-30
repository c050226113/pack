import json
import shelve
import sys
import threading
import os
import urllib.parse
from threading import Thread
import struct
import hashlib
import base64
import socket
import time
import subprocess
import redis

path = os.path.dirname(os.path.abspath(sys.argv[0]).replace('\\', '/')) + '/'
os.chdir(path)
for i in range(1, len(path.split('/')) - 2):
    sys.path.append(path + '../' * i)

from util.lib.Util import Util
from src.task.WatchPhp import WatchPhp
from util.lib.STD import STD
from src.task.WatchJs import WatchJs
from src.task.Build import Build
from src.lib.NormalPack import NormalPack
from ws4py.client.threadedclient import WebSocketClient
from util.lib.TIME import TIME


class returnCrossDomain(threading.Thread):
    def __init__(self, connection, task, file):
        Thread.__init__(self)
        self.con = connection
        self.isHandleShake = False
        self.masking = None
        self.payDataLength = None
        self.task = task
        self.file = file

    def run(self):
        while True:
            if not self.isHandleShake:
                # 开始握手阶段
                header = self.analyzeReq()
                secKey = header['Sec-WebSocket-Key']

                acceptKey = self.generateAcceptKey(secKey)

                response = "HTTP/1.1 101 Switching Protocols\r\n"
                response += "Upgrade: websocket\r\n"
                response += "Connection: Upgrade\r\n"
                response += "Sec-WebSocket-Accept: %s\r\n\r\n" % (acceptKey.decode('utf-8'))
                self.con.send(response.encode())
                self.isHandleShake = True
                STD.flush('response:\r\n' + response)
                # 握手阶段结束
            else:
                # 接受客户端数据
                opcode = self.getOpcode()
                if opcode == 8:
                    self.con.close()
                self.getDataLength()
                clientData = self.readClientData()
                # STD.flush('客户端数据：' + clientData)
                self.handle_data(clientData)
                # 向客户端发送数据
                # self.sendDataToClient('hello world')
            time.sleep(0.1)

    def handle_data(self, data):
        try:
            obj = json.loads(data)
            STD.flush(obj)
            self.task.append(obj)
        except:
            Util.err(data)

    def analyzeReq(self):
        reqData = self.con.recv(1024).decode()
        reqList = reqData.split('\r\n')
        headers = {}
        for reqItem in reqList:
            if ': ' in reqItem:
                unit = reqItem.split(': ')
                headers[unit[0]] = unit[1]
        return headers

    @staticmethod
    def generateAcceptKey(secKey):
        sha1 = hashlib.sha1()
        sha1.update((secKey + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode())
        sha1_result = sha1.digest()
        acceptKey = base64.b64encode(sha1_result)
        return acceptKey

    def getOpcode(self):
        first8Bit = self.con.recv(1)
        first8Bit = struct.unpack('B', first8Bit)[0]
        opcode = first8Bit & 0b00001111
        return opcode

    def getDataLength(self):
        second8Bit = self.con.recv(1)
        second8Bit = struct.unpack('B', second8Bit)[0]
        masking = second8Bit >> 7
        dataLength = second8Bit & 0b01111111

        if dataLength <= 125:
            payDataLength = dataLength
        elif dataLength == 126:
            payDataLength = struct.unpack('H', self.con.recv(2))[0]
        elif dataLength == 127:
            payDataLength = struct.unpack('Q', self.con.recv(8))[0]
        else:
            payDataLength = None
        self.masking = masking
        self.payDataLength = payDataLength

    def readClientData(self):
        if self.masking == 1:
            maskingKey = self.con.recv(4)
        else:
            maskingKey = ''

        data = self.con.recv(self.payDataLength)

        if self.masking == 1:
            index = 0
            trueData = ''
            for d in data:
                trueData += chr(d ^ maskingKey[index % 4])
                index += 1
            return trueData
        else:
            return data

    def sendDataToClient(self, text):
        sendData = struct.pack('!B', 0x81)

        length = len(text)
        if length <= 125:
            sendData += struct.pack('!B', length)
        elif length <= 65536:
            sendData += struct.pack('!B', 126)
            sendData += struct.pack('!H', length)
        elif length == 127:
            sendData += struct.pack('!B', 127)
            sendData += struct.pack('!Q', length)

        sendData += struct.pack('!%ds' % length, text.encode())
        dataSize = self.con.send(sendData)
        STD.flush('sendDataToClient:' + str(dataSize))


class DummyClient(WebSocketClient):
    def opened(self):
        pass
        #
        # @staticmethod
        # def closed(code, reason=None):
        #     print("Closed down", code, reason)
        #
        # @staticmethod
        # def received_message(m):
        #     print(m)


class ReadTask(threading.Thread):
    def __init__(self, task_q, file, ws, wsName):
        super().__init__()
        self.task_q = task_q
        self.file = file
        self.name = wsName
        STD.flush('debug: ' + wsName)
        self.ws = ws
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
        self.redis = redis.StrictRedis(connection_pool=pool)

    def run(self):
        flag = False
        while True:
            if len(self.task_q) > 0:
                task = self.task_q.pop()
                STD.flush(task)
                if 'file_dir' in task:
                    flag = True
                    task['file_dir'] = urllib.parse.unquote(task['file_dir'])
                if 'file_name' in task:
                    task['file_name'] = urllib.parse.unquote(task['file_name'])

                if 'type' in task:
                    if task['type'] == 'php':
                        WatchPhp(task, self.file)
                    elif task['type'] == 'js':
                        WatchJs(task, self.file)
                    elif task['type'] == 'build':
                        Build(task, self.redis)
                    else:
                        NormalPack(task).process()
            else:
                if len(self.task_q) <= 0 and flag is True:
                    flag = False
                    STD.flush('fresh')
                    try:
                        if self.ws['ws']:
                            self.ws['ws'].send(self.name)
                    except:
                        Util.err()
            time.sleep(0.5)


class ConnectWs(threading.Thread):
    def __init__(self, ws):
        super().__init__()
        self.ws = ws

    def run(self):
        try:
            # protocols=['chat']
            self.ws['ws'].run_forever()
        except:
            Util.err()
            self.ws['ws'].close()


class main:
    def __init__(self):
        self.file = shelve.open("../require_js.dat")
        self.task = list()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if 1 in sys.argv:
            self.port = int(sys.argv[1])
        else:
            self.port = 9002
        self.ws = {'ws': None}
        WsCreate(self.ws).start()
        time.sleep(2)

    def run(self):
        (ConnectWs(self.ws)).start()
        (ReadTask(self.task, self.file, self.ws, TIME.now())).start()
        self.sock.bind(('127.0.0.1', self.port))
        self.sock.listen(5)
        STD.flush('WebSocket server run...')
        while True:
            try:
                connection, address = self.sock.accept()
                returnCrossDomain(connection, self.task, self.file).start()
            except:
                Util.err()
            finally:
                time.sleep(0.1)

    def __del__(self):
        self.file.close()


class WsCreate(threading.Thread):
    def __init__(self, ws):
        super().__init__()
        self.ws = ws

    def run(self):
        self.ws['ws'] = DummyClient('wss://taurusgamer.com:8989/aaa')
        self.ws['ws'].connect()


class RunRedis(threading.Thread):
    def run(self):
        redis_server = os.path.abspath('../vendor/redis_2.4.5_64/redis-server.exe')
        child = subprocess.Popen(redis_server, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        STD.flush('redis run...')
        while True:
            time.sleep(10)
            # line = child.stdout.readline()
            if subprocess.Popen.poll(child) == 0:  # 判断子进程是否结束
                break


class RunHttpServer(threading.Thread):
    def run(self):
        if sys.argv[3]:
            php = os.path.abspath('../vendor/php-7.2.0-nts-Win32-VC15-x64/php.exe')
            child = subprocess.Popen(php + '-S 127.0.0.1:' + sys.argv[3], shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
            os.chdir(path)
            STD.flush('httpServer run...')
            while True:
                time.sleep(10)
                # line = child.stdout.readline()
                if subprocess.Popen.poll(child) == 0:  # 判断子进程是否结束
                    break


if __name__ == "__main__":
    RunRedis().start()
    RunHttpServer().start()
    main = main()
    main.run()
