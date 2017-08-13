#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

from ProxySites import BugngSpider, KuaiDaiLiSpider, SixSixipSpider, SuperfastipSpider, XiciSpider
from ProxySites import FreeProxyListsSpider, GatherproxySpider, ProxyNovaSpider
from validator import Validator
from redisdb import Redisdb
import queue
import time

target_url = "https://www.realestate.com.au"  # 必须是完整路径包含 http://等
Src_type = 0  # 0:'CN' 1:'EN'2:'ALL'
Proxy_type = "All"  # "All", "Http", "Https"


def proxy_server():
    proxy_queue = queue.Queue()

    redic_client = Redisdb()
    redic_client.init_proxy_table("")

    validator = Validator(target_url, redic_client, proxy_queue)
    validator.start()

    if Src_type == 0:
        proxy_src = [BugngSpider(proxy_queue, Proxy_type), KuaiDaiLiSpider(proxy_queue),
                     SixSixipSpider(proxy_queue, Proxy_type),
                     SuperfastipSpider(proxy_queue), XiciSpider(proxy_queue)]
    elif Src_type == 1:
        proxy_src = [FreeProxyListsSpider(proxy_queue), GatherproxySpider(proxy_queue), BugngSpider(proxy_queue),
                     ProxyNovaSpider(proxy_queue)]
    else:
        proxy_src = [BugngSpider(proxy_queue, Proxy_type), KuaiDaiLiSpider(proxy_queue),
                     SixSixipSpider(proxy_queue, Proxy_type),
                     SuperfastipSpider(proxy_queue), XiciSpider(proxy_queue), ProxyNovaSpider(proxy_queue),
                     FreeProxyListsSpider(proxy_queue), GatherproxySpider(proxy_queue), SixSixipSpider(proxy_queue)]

    while True:
        proxy_count = redic_client.get_proxy_count("")
        if proxy_count < 100:
            for src in proxy_src:
                src.start_requests()
        time.sleep(1)


if __name__ == '__main__':
    proxy_server()
