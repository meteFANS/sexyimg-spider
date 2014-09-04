#!/usr/bin/python  
# -*- coding:utf-8 -*-
import codecs
import hashlib
import json
import os
import urllib
import time
import sys
import re

__author__ = 'jeff'

if __name__ == '__main__':
    args = sys.argv

    if len(args) < 3:
        print 'ERROR:'
        print 'useage: python imgdownloader.py [input_json_file] [output_folder] [sleep_sec]'
        pass

    input_file = args[1]
    output_folder = args[2][-1:] == '/' and args[2] or args[2] + '/'
    sleep_sec = 0
    if len(args) == 4:
        sleep_sec = int(args[3])

    print 'DOWNLOAD START:'
    print '---------------------------'
    print 'input: ' + input_file
    print 'output: ' + output_folder
    print '---------------------------'

    file = codecs.open(input_file, 'r', encoding='utf-8')
    line = file.readline()

    while line:
        row = None
        try:
            row = json.loads(line)
        except Exception,e:
            print e
            continue
        finally:
            line = file.readline()

        imgname = ''.join(row['name'].encode('utf-8'))
        imgname = imgname.strip()

        if not imgname:
            continue

        if len(row['urls']) < 1:
            continue

        folder = output_folder + imgname
        if not os.path.exists(folder):
            os.makedirs(folder)
        domain = ''.join([n.encode('utf-8') for n in row['domain']])
        if domain[-1:] == '/':
            domain = domain[:-1]

        for k in row['urls']:
            i = k.encode('utf-8')

            if re.match(r'^(http://).*', i) is None:
                i = domain + i

            imgfile = folder + '/' + hashlib.sha1(i).hexdigest() + i[i.rfind('.'):]

            if os.path.exists(imgfile):
                if os.path.getsize(imgfile) == 0:
                    os.remove(imgfile)
                else:
                    continue
            try:
                time.sleep(sleep_sec)
                urllib.urlretrieve(i, imgfile)
                print '-> %s' % imgfile
            except Exception, e:
                if os.path.exists(imgfile):
                    os.remove(imgfile)
                print 'ERR: %s' % imgfile
                print e

    file.close()