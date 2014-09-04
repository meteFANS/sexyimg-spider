#!/usr/bin/python  
# -*- coding:utf-8 -*-
import hashlib
import os
import sys
import datetime
import pymongo
import subprocess

__author__ = 'jeff'


class ImgDao(object):
    def __init__(self, output):
        self.conn = pymongo.Connection('localhost', 27017)
        self.mydb = self.conn.sexyimg
        self.images = self.mydb.images

    def is_valid_img(self, path):
        if not os.path.exists(path):
            return False
        else:
            mypipe = subprocess.Popen('file "%s" |grep -i "image data"' % path, shell=True,
                                      stdout=subprocess.PIPE)
            if mypipe.returncode == 0:
                return len(mypipe.stdout.readline().strip()) > 0
            else:
                return False


    def add(self, name, img_paths, domain):

        imgs = []
        basefolder = hashlib.sha1(name).hexdigest()

        for img in img_paths:
            if self.is_valid_img(img):
                #todo move img file
                continue

        row = {
            'domain': domain,
            'name': name,
            'paths': img_paths,
            "time": datetime.datetime.now()
        }

        self.images.insert(row)

    pass


if __name__ == '__main__':
    print '---->' + mypipe.stdout.readline()







