#!/usr/bin/python  
# -*- coding:utf-8 -*-
import hashlib
import os
import shutil
import sys
import datetime
import pymongo
import subprocess

__author__ = 'jeff'


class ImgDao(object):
    '''mongodb图片数据存取接口'''

    def __init__(self, output, mongodb_host='127.0.0.1', mongodb_port=27017):
        self.conn = pymongo.Connection(mongodb_host, mongodb_port)
        self.mydb = self.conn.sexyimg
        self.images = self.mydb.images
        self.output = output

    def __del__(self):
        self.conn.close()


    def is_valid_img(self, path):
        if not os.path.exists(path) or os.path.isdir(path):
            return False
        else:
            mypipe = subprocess.Popen('file "%s" |grep -i "image data"' % path, shell=True,
                                      stdout=subprocess.PIPE)
            if mypipe.returncode == 0 or mypipe.returncode is None:
                return len(mypipe.stdout.readline().strip()) > 0
            else:
                return False


    def add(self, name, img_paths, from_domain):
        rname = name.strip()
        imgs = []
        folder_name = hashlib.sha1(rname).hexdigest()
        absolute_path = self.output + '/' + folder_name

        for img in img_paths:

            if not self.is_valid_img(img):
                continue

            if not os.path.exists(absolute_path):
                os.makedirs(absolute_path)

            bname = os.path.basename(img)
            dest_img_path = absolute_path + '/' + bname
            shutil.move(img, dest_img_path)
            imgs.append(bname)

        if len(imgs) < 1:
            print 'warn: empty folder[domain=%s,folder=%s]' % (from_domain, name)
            pass

        row = {
            'from': from_domain,  # 来源
            'name': rname,  # 组图名称
            'basedir': folder_name,  # 根路径
            'imgs': imgs,  # 图片文件列表
            'level': 0,  # 色情度0-10,越高越暴力
            'star': 0,  # 评价
            "time": datetime.datetime.now()  # 最后更新时间
        }

        self.images.insert(row)
        pass


def process_folder(folder, name, domain):
    paths = [folder + '/' + n for n in os.listdir(folder)]
    DAO.add(name, paths, domain)
    print '%s --> %s' % (domain, name)
    pass


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print 'useage: imgimport.py [input_path] [output_path]'
    else:
        rootdir = args[1]
        domains = os.listdir(rootdir)

        if len(domains) < 1:
            print 'ERROR: input folder is empty.'
            pass

        global DAO
        DAO = ImgDao('/home/jeff/bar')

        for domain in domains:
            for f in os.listdir(rootdir + '/' + domain):
                lastfolder = rootdir + '/' + domain + '/' + f
                name = f
                try:
                    process_folder(lastfolder, name, domain)
                except Exception, e:
                    print 'warn: ' + e
        pass






















