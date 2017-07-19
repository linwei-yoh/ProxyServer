#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'


from pyquery import PyQuery as pq
import re

from BaseProxySpider import BaseProxySpider
from proxy import Proxy
from logger_config import reportlog


class ProxyNovaSpider(BaseProxySpider):
    name = 'ProxyNova'

    def __init__(self,q):
        BaseProxySpider.__init__(self,q)

        self.urls = ["https://www.proxynova.com/proxy-server-list/elite-proxies/"]
        self.interval = 60 * 2

    def parse_page(self, response):
        proxy_list = list()

        try:
            doc = pq(response)
            table_node = doc("#tbl_proxy_list")
            item_nodes = table_node("tbody")("tr")
            for item in item_nodes.items():
                info_nodes = item("td:lt(2)")
                if len(info_nodes) < 2:
                    continue
                try:
                    proxy_item = [i.text() for i in info_nodes.items('td')]
                    params = re.findall(r"\D+([\d\\.]+)\D+(\d+)\D+([\d\\.]+)", proxy_item[0])[0]
                    ipstr1 = params[0]
                    ippos = int(params[1])
                    ipstr2 = params[2]

                    proxy = Proxy()
                    proxy.set_value(
                        ip=ipstr1[ippos:] + ipstr2,
                        port=proxy_item[1],
                        country='unkonw',
                        anonymity="elite proxy",
                        source=self.name,
                    )
                    proxy_list.append(proxy)
                except Exception:
                    pass
            self.add_proxys(proxy_list)
        except Exception as e:
            reportlog.error("%s 爬取出错:" % self.name + str(e))


if __name__ == '__main__':
    proxy_client = ProxyNova()
    proxy_client.start_requests()
    pass
