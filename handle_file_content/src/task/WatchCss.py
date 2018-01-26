from src.lib.NormalPack import NormalPack


class WatchCss:
    def __init__(self, task):
        normalPack = NormalPack(task)
        normalPack.process()
