import os
import traceback
import sys


class OS:
    @staticmethod
    def open_file(path, cmd):
        if not os.path.exists(path):
            return False
        else:
            try:
                return open(path, cmd)
            except:
                return False

    @staticmethod
    def make_dir(path):
        if os.path.exists(path):
            return True
        else:
            try:
                os.makedirs(path)
            except:
                print(traceback.format_exc())
                sys.stdout.flush()
            return True

    @staticmethod
    def open(file_path, op='r'):
        return open(file_path, op, encoding='utf-8')

    @staticmethod
    def rm_file(path):
        if os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)
