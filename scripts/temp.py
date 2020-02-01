#!/usr/bin/env/python

import os

INPUT_DIR = "/media/reggie/607049A4704981B0/compustat-10ks"
OUTPUT_DIR = "/media/reggie/607049A4704981B0/compustat-10ks-2"

url_index =  15

compustat_10ks = [x.strip().split('\t') for x in open('compustat-urls-db.txt','r').readlines()]
compustat_10ks = compustat_10ks[1:] ## Skip header
#current_url = compustat_10ks[0][url_index]
#f = current_url.split('/')[-1]

for _10k in compustat_10ks:
    current_url = _10k[url_index]
    f = current_url.split('/')[-1]
    os_command = "cp %s/%s %s/" % (INPUT_DIR, f, OUTPUT_DIR)
    os.system(os_command)
