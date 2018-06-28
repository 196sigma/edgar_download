#!/usr/bin/env python
import os
import re
import sys

def split_zips(filename_10k):
    ## Unzip and extract tar files
    os_command = "tar -xzf %s" % filename_10k
    ## extracts to a folder named /10k
    os.system(os_command)

    filename_10k = re.sub(r'\.tar\.gz', '', filename_10k)
    ## Make new directories
    os_command = "mkdir %s-01 && mkdir %s-02" % (filename_10k, filename_10k)
    os.system(os_command)

    ## Split files
    fileslist = os.listdir('10k')
    try:
        fileslist.remove('urls.txt')
    except:
        pass
    
    for x in fileslist[:3000]:
        os_command = "mv 10k/%s %s-01/" % (x, filename_10k)
        os.system(os_command)
        fileslist.remove(x)
    for y in fileslist:
        os_command = "mv 10k/%s %s-02/" % (y, filename_10k)
        os.system(os_command)

    ## tar and zip files
    os_command = "tar -czf %s-01.tar.gz %s-01/*" % (filename_10k, filename_10k)
    os.system(os_command)

    os_command = "tar -czf %s-02.tar.gz %s-02/*" % (filename_10k, filename_10k)
    os.system(os_command)

    ## Send back to S3
    os_command = "aws s3 cp %s s3://btcoal/10ks-2/" % (filename_10k+'-01.tar.gz')
    print os_command, os.system(os_command)
    
    os_command = "aws s3 cp %s s3://btcoal/10ks-2/" % (filename_10k+'-02.tar.gz')
    print os_command, os.system(os_command)

if __name__ == '__main__':
    filename_10k = sys.argv[1]
    split_zips(filename_10k)
