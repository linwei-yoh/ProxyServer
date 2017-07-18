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
        self.table_name = redis_config.free_ipproxy_table
        self.check_set = redis_config.ipproxy_check_set
        self.client = redis.StrictRedis(connection_pool=pool)

    def init_database(self, database_name):
        self.client.flushdb()

    def init_proxy_table(self, table_name):
        self.client.delete(self.table_name)

    def insert_proxy(self, table_name, proxy):
        data = proxy.get_dict()
        proxy_ip = data["ip"] + ":" + data["port"]
        if not self.client.sismember(self.check_set, proxy_ip):
            self.client.sadd(self.check_set, proxy_ip)
            self.client.rpush(self.table_name, json.dumps(data))

    def select_proxy(self, table_name, **kwargs):
        pass

    def delete_old(self, table_name, day):
        super().delete_old(table_name, day)

    def get_proxy_ids(self, table_name):
        super().get_proxy_ids(table_name)

    def del_proxy_with_id(self, table_name, id):
        super().del_proxy_with_id(table_name, id)

    def delete_proxy(self, table_name, proxy):
        super().delete_proxy(table_name, proxy)

    def del_proxy_with_ip(self, table_name, ip):
        super().del_proxy_with_ip(table_name, ip)

    def get_proxy_with_id(self, table_name, id):
        super().get_proxy_with_id(table_name, id)

    def update_proxy(self, table_name, proxy):
        super().update_proxy(table_name, proxy)

    def get_proxy_count(self, table_name):
        super().get_proxy_count(table_name)


if __name__ == '__main__':
    redis = Redisdb()
    pass
