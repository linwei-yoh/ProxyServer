# coding=utf-8

import urllib.parse
import re

from proxy import Proxy
from bs4 import BeautifulSoup
from BaseProxySpider import BaseProxySpider
import logging


class FreeProxyListsSpider(BaseProxySpider):
    name = 'freeproxylists'

    def __init__(self):
        BaseProxySpider.__init__(self)
        self.urls = ['http://www.freeproxylists.net/?c=&pt=&pr=&a%5B%5D=2&u=50']
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'www.freeproxylists.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

    def parse_page(self, response):
        proxy_list = list()
        try:
            pattern = re.compile('<tr class=(.*?)</tr>', re.S)
            items = re.findall(pattern=pattern, string=response)
            for i, item in enumerate(items):
                if i > 0:
                    if 'async' in item:
                        continue

                    ip_pattern = re.compile('IPDecode\(\"(.*?)\"\)', re.S)
                    ip_decode = re.findall(ip_pattern, item)[0]
                    ip_url = urllib.parse.unquote(ip_decode)
                    ip_soup = BeautifulSoup(ip_url, 'lxml')
                    ip = ip_soup.text

                    item = '<tr class=' + item + '</tr>'
                    soup = BeautifulSoup(item, 'lxml')
                    tbodys = soup.find_all('td')

                    proxy = Proxy()
                    proxy.set_value(
                        ip=ip,
                        port=tbodys[1].text,
                        country=tbodys[4].text,
                        anonymity=tbodys[3].text,
                        source=self.name,
                    )
                    proxy_list.append(proxy)

            self.add_proxys(proxy_list)
        except Exception as e:
            logging.error("%s 爬取出错:" % self.name + str(e))

if __name__ == '__main__':
    proxy_client = FreeProxyListsSpider()
    proxy_client.start_requests()
    pass
