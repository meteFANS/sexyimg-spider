#!/usr/bin/python  
# -*- coding:utf-8 -*-
import os
import sys

__author__ = 'caiweiwei'


def recursive_clean(yourfile):
    if not os.path.exists(yourfile):
        return

    if os.path.isdir(yourfile):
        subfiles = os.listdir(yourfile)
        for subfile in subfiles:
            foo = yourfile + '/' + subfile
            print foo
            recursive_clean(foo)
    elif yourfile.rfind('!') > -1:
        os.remove(yourfile)


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print 'useage: autocleaner.py [input_path]'
    else:
        rootdir = args[1]
        recursive_clean(rootdir)