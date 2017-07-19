#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'


from BaseProxySpider import BaseProxySpider

from pyquery import PyQuery as pq
from proxy import Proxy
from logger_config import reportlog


class KuaiDaiLiSpider(BaseProxySpider):
    name = '快代理'

    def __init__(self,q):
        BaseProxySpider.__init__(self,q)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'www.kuaidaili.com',
            'Upgrade-Insecure-Requests': '1',
        }
        self.urls = ["http://www.kuaidaili.com/free/inha/1/",
                     "http://www.kuaidaili.com/free/inha/2/",
                     "http://www.kuaidaili.com/free/inha/3/"]
        self.interval = 60 * 60  # 一小时一次

    def parse_page(self, response):
        proxy_list = list()

        try:
            doc = pq(response)
            item_list_node = doc('tr:gt(0)')

            for proxy_item in item_list_node.items():
                atts = [att.text() for att in proxy_item("td").items()]
                # IP:端口, 代理类型(Http/Https), 匿名性,  录入时间, 响应时间, 代理所在地
                country, *_ = atts[4].split(' ', 1)
                proxy = Proxy()
                proxy.set_value(
                    ip=atts[0],
                    port=atts[1],
                    country=country,
                    anonymity='elite proxy',
                    source=self.name,
                )
                proxy_list.append(proxy)
            self.add_proxys(proxy_list)
        except Exception as e:
            reportlog.error("%s 爬取出错:" % self.name + str(e))


if __name__ == '__main__':
    proxy_client = KuaiDaiLiSpider()
    proxy_client.start_requests()
    pass
