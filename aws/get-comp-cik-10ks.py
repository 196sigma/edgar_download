#!/usr/bin/env python

## Reginald Edwards
## 02 June 2017
## To be run on AWS.
## Send this file to each EC2 Ubuntu instance.
## Gets *ONLY* 10-Ks of firms with COMPUSTAT CIKs
## Gets downloaded 10-Ks from each EC2 instance and sends it to S3.
## Run with get-comp-cik-10ks-driver.py on local machine.

#get-comp-cik-10ks.py
import os
import sys
def get_compustat_10ks():        
    unzipped_files_dir = '/home/ubuntu/10k/data'
    output_dir = '/home/ubuntu/10k/compustat-10ks'
    files_10k = os.listdir(unzipped_files_dir)
    compustat_ciks = {}
    with open('/home/ubuntu/10k/compustat-ciks.txt','r') as infile:
        for line in infile:
            compustat_ciks[line.strip().split()[0]] = 1

    cik_file_map = {}
    for f in files_10k:
        cik = f.split('-')[0]
        if cik in compustat_ciks:
            cik_file_map[cik] = f
            os.system("cp %s %s" % (unzipped_files_dir+'/'+f, output_dir))
    return None

def send_to_s3(ec2_IP):
    s3_filename = "compustat-10ks-%s.tar.gz" % ec2_IP
    ## archive and compress
    os_command = "tar -czf %s /home/ubuntu/10k/compustat-10ks" % s3_filename
    os.system(os_command)
    ## send
    
    os_command = "aws s3 cp %s s3://redwards-10k/" % s3_filename
    os.system(os_command)
    
    return None
if __name__ == '__main__':
    ec2_IP = sys.argv[1]
    get_compustat_10ks()
    send_to_s3(ec2_IP)
