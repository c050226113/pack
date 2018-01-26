import os


class Build:
    def __init__(self, task, redis):
        self.root = task['root']
        self.dist = self.root + task['dist']
        self.redis = redis
        for src in task['src']:
            self.src = self.root + src
            self.for_each_src(self.src)

    def for_each_src(self, rootDir):
        _list = os.listdir(rootDir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(_list)):
            path = os.path.join(rootDir, _list[i])
            if os.path.isfile(path):
                new_path = path.replace(self.src, self.dist + 'src\\')
                if os.path.isfile(new_path):
                    pass
                else:
                    self.redis.publish('chat', path)
            else:
                self.for_each_src(path)
