# coding=utf-8

DB_config = {
    'db_type': 'redis',

    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'charset': 'utf8',
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'password': '',
        'db': 1,
    },
    'mongodb':{
        'host': 'localhost',
        'port': 27017,
        'username': '',
        'password': '',
    }
}

database = 'ipproxy'
ipproxy_check_set = "check_set"
free_ipproxy_table = 'free_ipproxy'
# httpbin_table = 'httpbin'
#
# data_port = 8000
