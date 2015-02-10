#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime
import pymongo

__author__ = 'caiweiwei'

GLOBAL_CONFIG = {
    'mongo_host': '127.0.0.1',
    'mongo_port': 27017,
    'daily_limit': 20
}

if __name__ == '__main__':
    conn = pymongo.Connection(GLOBAL_CONFIG['mongo_host'], GLOBAL_CONFIG['mongo_port'])
    db = conn['sexyimg']
    tbl = db['images']
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - datetime.timedelta(days=1)
    query = {
        'time': {'$gte': yesterday, '$lt': today},
        'flag': 9
    }
    rows = tbl.find(query)
    yesterday_count = rows.count()

    print 'yesterday_count = %d' % yesterday_count

    if rows.count() < 1:
        query = {'$or': [{'flag': None}, {'flag': 0}]}
        rows = tbl.find(query).limit(GLOBAL_CONFIG['daily_limit'])
        updated_time = yesterday.replace(hour=3)
        oids = []

        for row in rows:
            oids.append(row['_id'])

        if len(oids) > 0:
            tbl.update({'_id': {'$in': oids}}, {'$set': {'time': updated_time, 'level': 1, 'flag': 9}}, multi=True)

    conn.close()