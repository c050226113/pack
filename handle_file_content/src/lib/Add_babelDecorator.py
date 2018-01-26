import os
import subprocess

from util.lib.OS import OS
from util.lib.Util import Util


class Add_babelDecorator:
    def __init__(self, pack):
        try:
            # 打包babel
            f_new_path = pack.watch_file + '_new'
            print(f_new_path)
            f_new_fp = OS.open(f_new_path, 'w')
            f_new_fp.write(''.join(pack.lines))
            f_new_fp.close()

            f_babel_path = pack.watch_file + '_babel'

            cmd = 'babel %s -o %s' % (f_new_path, f_babel_path)
            child = subprocess.Popen(cmd, shell=True)
            child.wait()

            f_babel_fp = OS.open(f_babel_path)
            pack.lines = f_babel_fp.readlines(9999999)
            f_babel_fp.close()

            os.remove(f_new_path)
            os.remove(f_babel_path)
        except:
            Util.err()
