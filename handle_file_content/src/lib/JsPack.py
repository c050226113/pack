import os

from src.lib.NormalPack import NormalPack
from util.lib.OS import OS
from util.lib.Util import Util


class JsPack(NormalPack):
    def __init__(self, task, require):
        super().__init__(task)
        self.require = require
        self.require_js = set()

    def process(self):
        try:
            self.require[os.path.abspath(self.watch_file)] = self.require_js
            for parent in self.require:
                if os.path.abspath(self.watch_file) in self.require[parent]:
                    parent = parent.replace('\\dist', '')

                    f = OS.open(parent)
                    content = f.read(99999)
                    if content[-1:] == '\n':
                        content = content[:-1]
                    else:
                        content += '\n'
                    f.close()

                    f = OS.open(parent, 'w')
                    f.write(content)
                    f.close()
        except:
            Util.err()
        super().process()
