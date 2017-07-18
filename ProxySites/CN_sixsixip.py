#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from BaseProxySpider import BaseProxySpider
import re
from proxy import Proxy
import logging


class SixSixipSpider(BaseProxySpider):
    name = '66ip'

    def __init__(self):
        BaseProxySpider.__init__(self)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'www.66ip.cn',
            'Upgrade-Insecure-Requests': '1',
        }
        self.urls = [
            "http://www.66ip.cn/nmtq.php?"
            "getnum=200&"
            "isp=1&"
            "anonymoustype=3&"
            "start=&ports=&export=&ipaddress=&area=0&proxytype=0&"
            "api=66ip"]

    def parse_page(self, response):
        proxy_list = list()
        # re正则取出数据
        try:
            re_list_proxy = re.findall(r'(\d*\.\d*\.\d*\.\d*:\d*)', response)

            l = len(re_list_proxy)
            for i in range(l):
                ip, port = re_list_proxy[i].split(":", maxsplit=1)

                proxy = Proxy()
                proxy.set_value(
                    ip=ip,
                    port=port,
                    country='cn',
                    anonymity='elite proxy',
                    source=self.name,
                )
                proxy_list.append(proxy)
            self.add_proxys(proxy_list)
        except Exception as e:
            logging.error("%s 爬取出错:" % self.name + str(e))


if __name__ == '__main__':
    proxy_client = SixSixipSpider()
    proxy_client.start_requests()
    pass
