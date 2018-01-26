import os

import paramiko

from util.lib.OS import OS
from util.lib.STD import STD
from util.lib.Util import Util


class NormalPack:
    def __init__(self, task):
        self.watch_file = task['file_dir'] + task['file_name']
        self.watch_file_dir = task['file_dir']
        if not OS.is_file(self.watch_file):  # 删除操作
            exit()

        f = OS.open(self.watch_file)
        self.lines = f.readlines(99999)
        f.close()
        self.host = task['upload_host']  # 主机
        self.port = task['upload_port']  # 端口
        self.username = task['upload_user']  # 用户名
        self.password = task['upload_pwd']  # 密码
        self.upload_root = task['upload_root']  # 密码
        self.root = task['root']  # 密码

    def upload(self):
        sf = paramiko.Transport(self.host, self.port)
        sf.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(sf)
        try:
            if os.path.isdir(self.watch_file):  # 判断本地参数是目录还是文件
                for f in os.listdir(self.watch_file):  # 遍历本地目录
                    sftp.put(os.path.join(self.watch_file + f), os.path.join(self.watch_file + f))  # 上传目录中的文件
            else:
                remote = self.upload_root + self.watch_file.split(self.root)[1]
                here = self.watch_file
                STD.flush(here)
                STD.flush(remote)
                sftp.put(here, remote)  # 上传文件
        except:
            Util.err()
        sf.close()

    def process(self):
        f = OS.open(self.watch_file, 'w')
        f.write(''.join(self.lines))
        f.close()
        if self.host != '127.0.0.1':
            STD.flush('start upload')
            self.upload()
