import re

import os


class Add_css_hashDecorator:
    def __init__(self, pack):
        self.pack = pack
        for i, line in enumerate(self.pack.lines):
            pattern = 'href="(.*\.css).*"'
            res = re.findall(pattern, line)
            if len(res) <= 0:
                continue

            s = res[0]
            if s.startswith('http'):
                continue

            css_path = self.pack.watch_file_dir + s
            ctime = str(os.path.getctime(css_path))
            self.pack.lines[i] = re.sub('href=".*\.css.*"', 'href="' + s + '?v=' + ctime + '"', line)
