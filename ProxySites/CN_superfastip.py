#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from BaseProxySpider import BaseProxySpider
import re

import logging
from proxy import Proxy


class SuperfastipSpider(BaseProxySpider):
    name = 'superfast'

    def __init__(self):
        BaseProxySpider.__init__(self)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'superfastip.com',
            'Upgrade-Insecure-Requests': '1',
            "Referer": "http://superfastip.com/welcome/getips",
        }
        self.urls = ["http://superfastip.com/welcome/getips/1",
                     "http://superfastip.com/welcome/getips/2"]

    def parse_page(self, response):
        proxy_list = list()
        # re正则取出数据
        try:
            response = response.encode('ISO-8859-1').decode()
            re_list_item = re.findall(r'<tr>(.*?)</tr>', response, re.S)
            l = len(re_list_item)
            for i in range(l):
                atts = re.findall(r'<td>(.*?)</td>', re_list_item[i], re.S)

                proxy = Proxy()
                proxy.set_value(
                    ip=atts[1],
                    port=atts[2],
                    country=atts[0],
                    anonymity='elite proxy',
                    source=self.name,
                )
                proxy_list.append(proxy)
            self.add_proxys(proxy_list)
        except Exception as e:
            logging.error("%s 爬取出错:" % self.name + str(e))


if __name__ == '__main__':
    proxy_client = SuperfastipSpider()
    proxy_client.start_requests()
    pass
