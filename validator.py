#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import requests
from utilities import make_random_useragent
from logger_config import ip_log, reportlog


class Validator(Thread):
    def __init__(self, tar_url, client, proxy_queue):
        Thread.__init__(self, name="validator", daemon=True)
        self.target_url = tar_url
        self.proxy_queue = proxy_queue
        self.client = client
        self.recoder = {}

    def run(self):
        print("解析线程池启动")
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                try:
                    proxy = self.proxy_queue.get(block=True)
                    executor.submit(self.proxy_check, proxy)
                except Exception as e:
                    reportlog.error(e)

    def proxy_check(self, proxy):
        proxy_ip = proxy.get_ip_port()
        try:
            proxies = {
                "http": "http://%s" % proxy_ip,
                "https": "http://%s" % proxy_ip,
            }
            header = {'User-Agent': make_random_useragent()}
            r = requests.get(self.target_url, headers=header, proxies=proxies, timeout=(6.05, 10))
        except Exception as e:
            return None

        if r.status_code == 200:
            if proxy.source not in self.recoder:
                self.recoder[proxy.source] = 1
            else:
                self.recoder[proxy.source] += 1
            ip_log.warning(self.recoder)
            self.client.insert_proxy("", proxy_ip)


if __name__ == '__main__':
    pass
