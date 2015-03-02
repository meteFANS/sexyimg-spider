#!/usr/bin/python  
# -*- coding:utf-8 -*-
import os
import pymongo
import sys

__author__ = 'caiweiwei'

GLOBAL_CONFIG = {
    'mongo_host': '127.0.0.1',
    'mongo_port': 27017
}

conn = pymongo.Connection(GLOBAL_CONFIG['mongo_host'], GLOBAL_CONFIG['mongo_port'])
db = conn['sexyimg']
tbl = db['images']


def img_exists(folder):
    one = tbl.find_one({'basedir': folder}, {})
    return one and True or False


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print 'useage: autocleaner.py [input_path]'
    else:
        rootdir = args[1]
        basedirs = os.listdir(rootdir)
        for basedir in basedirs:
            if os.path.isdir(rootdir + '/' + basedir) and not img_exists(basedir):
                os.removedirs(rootdir + '/' + basedir)
    conn.close()