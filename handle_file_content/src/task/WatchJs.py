from src.lib.Add_babelDecorator import Add_babelDecorator
from src.lib.Add_js_hashDecorator import Add_js_hashDecorator
from src.lib.Add_tplDecorator import Add_tplDecorator
from src.lib.JsPack import JsPack
from util.lib.STD import STD


class WatchJs:
    def __init__(self, task, require):
        file = JsPack(task, require)
        Add_js_hashDecorator(file)
        Add_tplDecorator(file)
        Add_babelDecorator(file)
        file.process()
