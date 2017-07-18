#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from BaseProxySpider import BaseProxySpider
import logging
import json
from proxy import Proxy


class BugngSpider(BaseProxySpider):
    name = '虫代理'

    def __init__(self):
        BaseProxySpider.__init__(self)
        self.urls = ["http://www.bugng.com/api/getproxy/json?num=80&anonymity=1&type=0"]
        self.interval = 30  # 0.5分钟

    def parse_page(self, response):
        proxy_list = list()
        # re正则取出数据
        try:
            json_data = json.loads(response)
            proxy_item_list = json_data["data"]["proxy_list"]
            for proxy_item in proxy_item_list:
                ip, port = proxy_item.split(":", maxsplit=1)
                proxy = Proxy()
                proxy.set_value(
                    ip=ip,
                    port=port,
                    country="cn",
                    anonymity='elite proxy',
                    source=self.name,
                )
                proxy_list.append(proxy)
            self.add_proxys(proxy_list)
        except Exception as e:
            logging.error("%s 爬取出错:" % self.name + str(e))


if __name__ == '__main__':
    proxy_client = BugngSpider()
    proxy_client.start_requests()
    pass
