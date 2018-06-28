#!/usr/bin/env python

import os

EXT_LOC = '/media/reggie/607049A4704981B0'
TEMP_DIR = EXT_LOC + '/temp'
UNZIP_DIR = TEMP_DIR + '/10k'
OUTPUT_DIR = EXT_LOC + '/compustat-10ks'
INPUT_DIR = EXT_LOC + '/compustat-10ks-zipped'

zipfiles_list = ['10ks-54.200.44.106.tar.gz',
                 '10ks-54.201.13.134.tar.gz',
                 '10ks-54.202.110.208.tar.gz',
                 '10ks-54.212.211.170.tar.gz',
                 '10ks-54.214.119.90.tar.gz',
                 '10ks-54.214.214.102.tar.gz',
                 '10ks-54.214.214.159.tar.gz',
                 '10ks-54.214.226.224.tar.gz',
                 '10ks-54.218.20.218.tar.gz',
                 '10ks-54.218.41.151.tar.gz']

for zipfile in zipfiles_list:
    os_command = "tar -xzf %s/%s -C %s" % (INPUT_DIR, zipfile, TEMP_DIR)
    print os_command
    print os.system(os_command)

    os_command = "mv %s/* %s" % (UNZIP_DIR, OUTPUT_DIR)
    os.system(os_command)
    with open('already-done.txt','a') as outfile:
        outfile.write(zipfile+'\n')

    ## Clean up
    os_command = "rm -r %s" % UNZIP_DIR
    print os_command
    print os.system(os_command)
