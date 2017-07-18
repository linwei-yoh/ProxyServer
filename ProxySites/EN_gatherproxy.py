# coding=utf-8

import json
import re


from BaseProxySpider import BaseProxySpider
from proxy import Proxy
import logging


class GatherproxySpider(BaseProxySpider):
    name = 'gatherproxy'

    def __init__(self):
        BaseProxySpider.__init__(self)
        self.urls = [
            'http://gatherproxy.com/',
            'http://www.gatherproxy.com/proxylist/anonymity/?t=Anonymous',
            'http://gatherproxy.com/proxylist/country/?c=China',
        ]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'www.gatherproxy.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

    def parse_page(self, response):
        proxy_list = list()
        try:
            pattern = re.compile('gp.insertPrx\((.*?)\)', re.S)
            items = re.findall(pattern, response)
            for item in items:
                data = json.loads(item)
                # 端口用的是十六进制
                port = data.get('PROXY_PORT')
                port = str(int(port, 16))

                proxy = Proxy()
                proxy.set_value(
                    ip=data.get('PROXY_IP'),
                    port=port,
                    country=data.get('PROXY_COUNTRY'),
                    anonymity=data.get('PROXY_TYPE'),
                    source=self.name,
                )
                proxy_list.append(proxy)
            self.add_proxys(proxy_list)
        except Exception as e:
            logging.error("%s 爬取出错:" % self.name + str(e))


if __name__ == '__main__':
    proxy_client = GatherproxySpider()
    proxy_client.start_requests()
    pass

