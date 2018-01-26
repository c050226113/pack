import time
from urllib import request
import requests

from util.lib.Util import Util


class NET:
    @staticmethod
    def get(url):
        response = request.urlopen(url)
        return response.read().decode('utf-8', 'ignore')

    def post(self):
        pass

    @staticmethod
    def browser_get(url, req_header=None):
        try:
            req = requests.get(url, headers=req_header)
            if req.encoding == 'ISO-8859-1':
                encodings = requests.utils.get_encodings_from_content(req.text)
                if encodings:
                    encoding = encodings[0]
                else:
                    encoding = req.apparent_encoding
            else:
                encoding = req.apparent_encoding
            encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
            return encode_content.decode('utf-8', 'ignore')
        except:
            Util.err()
            return ''

    @staticmethod
    def continue_browser_get(url, count=1, ref=None):
        counter = 0
        while 1:
            if counter > count:
                break
            try:
                if ref:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/58.0.3029.110 Safari/537.36',
                        'Accept': 'text/html;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        # 'Accept-Encoding': 'gzip',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        # # 'X-Forwarded-For': Util.get_random_ip(),
                        # 'Connection': 'close',
                        # 'Cache-Control': 'no-cache',
                        'Referer': ref
                    }
                    req = request.Request(url, headers=headers)
                    response = request.urlopen(req)
                    res_str = response.read().decode('utf-8', 'ignore')
                else:
                    response = request.urlopen(url)
                    res_str = response.read().decode('utf-8', 'ignore')
                return res_str
            except Exception as e:
                Util.err()
                print(url)
                if str(e) == 'HTTP Error 404: Not Found':
                    counter += 1
                    continue
                if str(e) == 'Remote end closed connection without response':
                    time.sleep(1)
                    continue
                if str(e) == 'HTTP Error 502: Bad Gateway':
                    time.sleep(1)
                    continue
                if str(e) == 'HTTP Error 500: Internal Server Error':
                    time.sleep(1)
                    continue
            counter += 1
        return False
