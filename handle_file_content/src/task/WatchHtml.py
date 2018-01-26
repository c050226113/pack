from src.lib.NormalPack import NormalPack


class WatchHtml:
    def __init__(self, task):
        normalPack = NormalPack(task)
        normalPack.process()
