# coding=utf-8


import requests
from datetime import datetime
import time

from concurrent.futures import ThreadPoolExecutor
import utilities


# def make_dir(dir):
#     if not os.path.exists(dir):
#         os.makedirs(dir)


class BaseProxySpider(object):
    name = 'basespider'

    def __init__(self):
        self.urls = []
        # self.dir_log = 'log/proxy/%s' % self.name
        self.headers = {}
        self.start = True
        self.last_time = datetime.now()
        self.interval = 60 * 10  # 10分钟

    def start_requests(self):
        if self.interval is None:
            pass
        elif (datetime.now() - self.last_time).total_seconds() >= self.interval:
            self.last_time = datetime.now()
            self.start = True

        if self.start:
            self.start = False

            with ThreadPoolExecutor(max_workers=5) as executor:
                for url in self.urls:
                    executor.submit(self.fetch_page, url).add_done_callback(self.check_and_parse)
                    time.sleep(1)

    def fetch_page(self, url):
        try:
            self.headers["User-Agent"] = utilities.make_random_useragent()
            r = requests.get(url, headers=self.headers, timeout=(6.05, 10))
        except Exception:
            return None
        else:
            if r.status_code == 200:
                return r.text
            else:
                return None

    def check_and_parse(self, content):
        response = content.result()
        if response is None:
            pass
        else:
            self.parse_page(response)

    def parse_page(self, content):
        pass

    def error_parse(self, failure):
        request = failure.request
        pass

    def add_proxys(self, proxys):
        print(len(proxys))
        pass
