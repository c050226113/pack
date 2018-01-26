import sys

from util.lib.OS import OS


class STD:
    @staticmethod
    def out(string, path=None):
        if path is not None:
            f = OS.open(path, 'a')
            f.write(string + '\n')
            f.close()
        else:
            print(string)

    @staticmethod
    def die(string=''):
        STD.out(string)
        exit()

    @staticmethod
    def flush(string):
        print(string)
        sys.stdout.flush()
