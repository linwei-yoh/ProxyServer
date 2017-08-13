#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'AL'

import logging
import redis
import config
from sql_base import SqlBase
import json


class Redisdb(SqlBase):
    def __init__(self, **kwargs):
        super(Redisdb, self).__init__(**kwargs)

        redis_config = config.DB_config.get("redis", None)
        pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'], db=redis_config["db"])
        self.table_name = config.free_ipproxy_table
        self.check_set = config.ipproxy_check_set
        self.client = redis.StrictRedis(connection_pool=pool)
        print("redis 链接完成")

    def init_proxy_table(self, table_name):
        self.client.delete(self.check_set)
        self.client.delete(self.table_name)
        print("清除全部proxy记录")

    def insert_proxy(self, table_name, proxy:str):
        if not self.client.sismember(self.check_set, proxy):
            self.client.sadd(self.check_set, proxy)
            self.client.lpush(self.table_name, proxy)

    def update_proxy(self, table_name, proxy):
        self.client.rpush(self.table_name, proxy)

    def get_proxy_count(self, table_name):
        return self.client.llen(self.table_name)


if __name__ == '__main__':
    redis = Redisdb()
    redis.init_proxy_table("")
    pass
