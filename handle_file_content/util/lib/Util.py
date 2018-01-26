import codecs
import gzip
import hashlib
import json
import os
import random
import re
import shlex
import subprocess
import time
import traceback
from urllib import parse
from collections import OrderedDict
from io import StringIO
from pprint import pprint

import requests
from lxml.html import HTMLParser

from util.lib.OS import OS
from util.lib.STD import STD
from util.lib.TYPE import TYPE


class Util:
    @staticmethod
    def is_all_zero(_set):
        for val in _set:
            if val != 0:
                return False
        return True

    @staticmethod
    def err(e=None):
        if e:
            print(e)
        STD.flush(traceback.format_exc())

    @staticmethod
    def check_gzip(data, keyword):
        if data.find(keyword) is -1:
            data = Util.gzdecode(data)
        return data

    @staticmethod
    def quote(data):
        return parse.quote(data)

    @staticmethod
    def print_l(string):
        print(string + "\n")

    @staticmethod
    def replace_space(string):
        return string.replace('\r', '').replace('\n', '').replace(' ', '')

    @staticmethod
    def trim_all(string):
        return Util.replace_space(str(string))

    @staticmethod
    def trim(string):
        return string.lstrip(' \n\r\n').rstrip(' \n\r\n')

    @staticmethod
    def has_other_country_letter(string):
        res = re.search(r"[\u2E80-\uFFFDh]", string)
        if res is not None:
            return True
        else:
            return False

    @staticmethod
    def get_random_ip():
        ip_list = list()
        ip_list.append(str(random.randint(2, 120)))
        ip_list.append(str(random.randint(10, 254)))
        ip_list.append(str(random.randint(10, 254)))
        ip_list.append(str(random.randint(10, 254)))
        return '.'.join(ip_list)

    @staticmethod
    def gzdecode(data):
        stream = StringIO(data)
        gziper = gzip.GzipFile(fileobj=stream)
        return gziper.read()

    file_dict = dict()

    @staticmethod
    def append_data(file_path, content):
        if file_path not in Util.file_dict or Util.file_dict[file_path].closed or not Util.file_dict[file_path]:
            Util.file_dict[file_path] = OS.open(file_path, "a")
        Util.file_dict[file_path].write(content)

    @staticmethod
    def all_file_flush():
        for file_path in Util.file_dict:
            if Util.file_dict[file_path].closed:
                Util.file_dict[file_path] = OS.open(file_path, "a")
            Util.file_dict[file_path].flush()

    @staticmethod
    def http_get(url_root, tail, try_cnt=1):
        url = 'http://' + url_root + tail
        continueTimes = 0
        while True:
            try:
                if continueTimes >= try_cnt:
                    return False

                req = requests.get(url)
                if not req.text:
                    continueTimes += 1
                    continue
                return req.text
            except:
                Util.err()
                continueTimes += 1

    @staticmethod
    def tup_join(tup, split=''):
        string = ""
        length = len(tup)
        count = 0
        for item in tup:
            count += 1
            string += str(item) + ('' if count >= length else split)
        return string

    @staticmethod
    def read_each_line(file_path, func=None):
        if func is None:
            return
        fp = OS.open(file_path, "r")
        for line in fp:
            func(line)
        fp.close()

    @staticmethod
    def die(string):
        Util.print_r(string)
        exit()

    @staticmethod
    def once_read_cnt(fname, read_size):
        f = OS.open(fname, "r")
        while True:
            block = f.read(read_size)
            if block:
                yield block
            else:
                f.close()
                return

    @staticmethod
    def read_reverse(file_path, func=None):
        file_no_break_path = file_path + '_no_break'
        OS.open(file_no_break_path, 'w').close()
        once_read_size = 3333333
        f = OS.open(file_no_break_path, 'a')
        for block in Util.once_read_cnt(file_path, once_read_size):
            block = block.replace("\n", '{{{')
            f.write(block)
        f.close()

        f = codecs.open(file_no_break_path, encoding='utf-8')
        f.seek(0, os.SEEK_END)
        last_position = f.tell()
        last = ''
        val = 1
        isEnd = False
        time1 = Util.time()
        content = ''
        while 1:
            last_position -= val
            if last_position < 0:
                val = val + last_position
                last_position = 0
                isEnd = True
            f.seek(last_position)
            try:
                print('content:' + content)
                content = f.read(val)
            except:
                Util.err('content:' + content)
                exit()
            _list = content.split('{{{')
            _list.reverse()
            _list[0] = _list[0] + last
            last = _list.pop()
            func(_list)
            if isEnd:
                func([last])
                break
        f.close()
        print('kill_time:' + str(int(time.time()) - time1))
        os.remove(file_path)
        os.remove(file_no_break_path)

    @staticmethod
    def get_key(key, dic, default=''):
        try:
            if (TYPE.is_list(key) and len(key) <= 1) or TYPE.is_str(key):
                if TYPE.is_list(key):
                    key = str(key[0])
                if key in dic:
                    return dic[key]
                else:
                    return default
            else:
                dic = Util.get_key(key[0], dic)
                if TYPE.is_dict(dic):
                    key.pop(0)
                    return Util.get_key(key, dic)
                else:
                    return default
        except:
            Util.err()
            return default

    @staticmethod
    def getElementByTagAndAttr(nodeObj, tagName, attrName=None, attrVal=None, content=False):
        # 以下这个是正则匹配，正则表达式比较难以理解
        if attrName is None:
            reLeft = re.compile(r'''(\<%s[^\<\>]*?\>)''' % (tagName))
        else:
            reLeft = re.compile(r'''((?:\<%s[^\<\>]*?%s=['"]%s['"][^\<\>]*?\>))''' % (tagName, attrName, attrVal))
        reRight = re.compile(r'<%s\W|</%s>' % (tagName, tagName))
        endR = '</%s>' % (tagName)
        pos = 0
        ret = []
        while True:
            mL = reLeft.search(nodeObj, pos)
            if mL is None:
                break
            pos = mL.end(0)
            count = 1
            while True:
                mR = reRight.search(nodeObj, pos)
                if mR is None:
                    return None
                pos = mR.end(0)
                if mR.group(0) == endR:
                    count -= 1
                else:
                    count += 1
                if count == 0:
                    if content:
                        ret.append(nodeObj[mL.end(0):mR.start(0)])
                    else:
                        ret.append(nodeObj[mL.start(0):mR.end(0)])
                    break
        return ret

    @staticmethod
    def get_html_tag_content(html, tag):
        reg = '<' + tag + '>(.*?)</' + tag + '>'
        reObj = re.compile(reg, re.I | re.M)
        result = reObj.search(html)
        if result is None:
            return ''
        else:
            return result.group(1)

    @staticmethod
    def get_html_attr(html, attr):
        reg = attr + '="(.*?)"'
        reObj = re.compile(reg, re.I | re.M)
        result = reObj.search(html)
        if result is None:
            return ''
        else:
            return result.group(1)

    @staticmethod
    def kill_repeat(split_char, path_old, index_arr=None):
        if index_arr is None:
            index_arr = [0]
        print('kill_path:' + path_old)
        if path_old in Util.file_dict:
            Util.file_dict[path_old].close()
        lines = set()
        need_key = len(index_arr)
        path_new = path_old + '_repeat'
        if os.path.exists(path_old):
            OS.open(path_new, 'w').close()
            OS.rm_file(path_new)
            os.rename(path_old, path_new)
        else:
            return lines

        start = Util.time()

        new = OS.open(path_new)
        old = OS.open(path_old, 'a')

        def add_file():
            now_file = OS.open('tmp_' + str(now_index), 'w')
            now_file.write(chr(5).join(stack))
            now_file.close()

        stack = []
        now_index = 0
        count = 0
        for line in new:
            stack.append(line)
            if count > 200000:
                count = 0
                add_file()
                now_index += 1
                stack = []
            count += 1
        add_file()

        max_index = now_index

        def handle_line(_line):
            if len(_line) < 2:
                return
            lineArr = _line.split(split_char)
            try:
                if need_key > 1:
                    unique_id = Util.get_unique_id(lineArr[index_arr[0]], lineArr[index_arr[1]])
                else:
                    unique_id = Util.get_unique_id(lineArr[index_arr[0]])
            except:
                Util.err(_line)
                return
            if unique_id not in lines:
                lines.add(unique_id)
                old.write(_line)

        while now_index >= 0:
            stack = OS.open('tmp_' + str(now_index), 'r').read().split(chr(5))
            while len(stack) > 0:
                handle_line(stack.pop())
            now_index -= 1

        old.close()
        new.close()

        for i in range(max_index, -1, -1):
            print('./tmp_' + str(i))
            os.remove('./tmp_' + str(i))
        print(Util.time() - start)

        os.remove(path_new)
        return lines

    @staticmethod
    def get_unique_id(small, big=''):
        if big != '':
            big_list = map(lambda x: int(x), str(big).split('|'))
            big = sum(big_list)
            big = int(str(big) + '000000000000000')
            return big + int(small)
        else:
            return int(small)

    @staticmethod
    def now():
        return str(int(time.time()))

    @staticmethod
    def time():
        return int(time.time())

    @staticmethod
    def print_r(dic):
        pprint(dic)

    @staticmethod
    def is_test():
        shell_cmd = 'uname -n'
        cmd = shlex.split(shell_cmd)
        child = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        child.wait()
        res = map(lambda line: line.decode('utf-8', 'ignore'), child.stdout.readlines())
        res = ''.join(res)
        if res.find('test') > 0:
            return True
        else:
            return False

    @staticmethod
    def md5(_str):
        GenMD5 = hashlib.md5()
        GenMD5.update(_str.encode('utf-8'))
        return GenMD5.hexdigest()

    @staticmethod
    def hex2dec(_str):
        return str(int(_str, 16))

    @staticmethod
    def get_now_year():
        time_array = time.localtime(int(time.time()))
        return int(time.strftime("%Y", time_array))

    @staticmethod
    def addslashes(string):
        if string.find('\\') >= 0:
            string = string.replace('\\', '')
        if string.find("'") >= 0:
            string = string.replace("'", "\\'")
            # string = string.replace("\\\\'", "\\'")
        if string.find('"') >= 0:
            string = string.replace('"', '\\"')
            # string = string.replace('\\\\"', '\\"')
        return string

    single_num_dict = {
        u'零': 0,
        u'一': 1,
        u'二': 2,
        u'三': 3,
        u'四': 4,
        u'五': 5,
        u'六': 6,
        u'七': 7,
        u'八': 8,
        u'九': 9,
        u'十': 10
    }

    @staticmethod
    def chinese2num(chinese):
        reg = u'[十百千]'
        e = re.compile(reg)
        result_list = e.findall(chinese)
        if len(result_list) > 0:
            tmp = None
            ge = 0
            num = OrderedDict()
            num[u"十"] = None
            num[u"百"] = None
            num[u"千"] = None

            if chinese[:1] == '十':
                chinese = '一' + chinese

            for letter in chinese:
                if letter != '十' and letter != '百' and letter != '千':
                    tmp = Util.single_num_dict[letter]
                else:
                    num[letter] = tmp
                    tmp = None

            if tmp is not None:
                index = 0
                for key in num:
                    if num[key] is not None:
                        break
                    index += 1

                if index <= 0:
                    ge = tmp
                else:
                    bingo_index = index - 1
                    index = 0
                    for key in num:
                        if index == bingo_index:
                            num[key] = tmp
                            break
                        index += 1

            for key in num:
                if num[key] is None:
                    num[key] = 0

            return str(num[u"十"] * 10 + num[u"百"] * 100 + num[u"千"] * 1000 + ge)
        else:
            result = ''
            for letter in chinese:
                result += str(Util.single_num_dict[letter])
            return result

    @staticmethod
    def translate_html_special_characters(string):
        html_parser = HTMLParser()
        print(dir(html_parser))
        data = '<br>'
        print(html_parser.feed(data))
        print(data)
        return html_parser.parse(string)

    @staticmethod
    def has_other_country_word(string):
        search = re.search(
            r"[\u3040-\u30FF]|[\u31F0-\u31FF]|[\u1100-\u11FF]|[\u3130-\u318f]|[\uac00-\ud7af]",
            string)
        if search is not None:
            return search
        else:
            return False

    @staticmethod
    def no_chinese(string):
        search = re.search(r"[\u4e00-\u9fa5]", string)
        if search is None:
            return True
        else:
            return False

    @staticmethod
    def two_sentence_similar_rate(a, b):
        a_set = set()
        b_set = set()
        for letter in a:
            a_set.add(letter)
        for letter in b:
            b_set.add(letter)

        return len(a_set & b_set) / len(a)

    @staticmethod
    def get_Gjson(_input):
        res = _input
        try:
            i = 1
            for i, letter in enumerate(res[::-1]):
                if letter == '}':
                    break
            res = str(res[res.index('(') + 1:i*-1])
            return json.loads(res)
        except:
            Util.err(_input)
            return ''
