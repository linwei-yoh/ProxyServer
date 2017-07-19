#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from BaseProxySpider import BaseProxySpider
import re
from proxy import Proxy

from logger_config import reportlog


class XiciSpider(BaseProxySpider):
    name = 'xicidaili'

    def __init__(self,q):
        BaseProxySpider.__init__(self,q)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'www.xicidaili.com',
            'Upgrade-Insecure-Requests': '1',
            "Referer": "http://www.xicidaili.com/",
        }
        self.urls = ["http://www.xicidaili.com/nn/1",
                     "http://www.xicidaili.com/nn/2",
                     "http://www.xicidaili.com/nn/3",
                     "http://www.xicidaili.com/nn/4"]
        self.interval = 60 * 60 * 5 # 5小时

    def parse_page(self, response):
        proxy_list = list()
        # re正则取出数据
        try:
            re_list_ip = re.findall(r'<td>(\d*\.\d*\.\d*\.\d*)</td>', response)
            re_list_port = re.findall(r'<td>([\d]*)</td>', response)

            l = len(re_list_ip)
            for i in range(l):
                proxy = Proxy()
                proxy.set_value(
                    ip=re_list_ip[i],
                    port=re_list_port[i],
                    country='cn',
                    anonymity='elite proxy',
                    source=self.name,
                )
                proxy_list.append(proxy)

            self.add_proxys(proxy_list)
        except Exception as e:
            reportlog.error("%s 爬取出错:" % self.name + str(e))


if __name__ == '__main__':
    proxy_client = XiciSpider()
    proxy_client.start_requests()
    pass
