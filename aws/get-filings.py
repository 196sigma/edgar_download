#!/usr/bin/env python
## Reginald Edwards
## 02 June 2017
## Run on local machine
## Take list of 10-K filings URLs, split based on the number of EC2 instances, and download
## TODO:
##   - move tar and send_to_s3 functions to separate modules

import os
import boto3
import time
AMI_ID = "ami-8171f2e1"
SEC_GROUP_ID='sg-f9d54281'
N_INSTANCES = 9
#FS_ID = 'fs-eadb1443'

# Location of URLs on local system that are to be downloaded over EC2 instances
#FILINGS_URLS = '/home/reggie/Dropbox/Research/0_datasets/sec-10k-urls-sample.txt'
#FILINGS_URLS = '/home/reggie/Dropbox/Research/0_datasets/sec-10k-urls.txt'
FILINGS_URLS = 'sample-compustat-urls.txt'

PEM_KEY_LOC = '/home/reggie/Dropbox/aws/aws-key.pem'

def send_urls_helper(start_index, stop_index, ec2_IP):
    ## create file name for sample of URLs to be sent to this EC2 instance
    urls_sample_filename = "/tmp/urls-%s.txt" % ec2_IP

    ## Get sample of URLs to send to this EC2 instance
    urls = open(FILINGS_URLS,'r').readlines()
    urls = urls[start_index:stop_index]
    with open(urls_sample_filename,'w') as outfile:
        outfile.writelines(urls)
        
    ## Send URLs file to EC2 instance
    os_command = "scp -o UserKnownHostsFile=~/Dropbox/aws/aws_khosts -o StrictHostKeyChecking=no -i %s %s ubuntu@%s:10k/urls.txt" % (PEM_KEY_LOC, urls_sample_filename, ec2_IP)
    print os.system(os_command), os_command
    return None

## Split large URLs file into equal-sized chunks and send to each EC2 instance
def send_urls(ec2_instance_list=[], urls_location=""):
    n_instances = len(ec2_instance_list)
    urls = open(urls_location,'r').readlines()
    n_files = len(urls)
    sample_size = n_files/n_instances
    print '%d files, %d instances, %d files per instance' % (n_files, n_instances, sample_size)
    i = 0
    while i < (n_instances-1):
        send_urls_helper(i*sample_size, (1+i)*(sample_size), ec2_instance_list[i])
        i += 1
    if i == (n_instances-1):
        send_urls_helper(i*sample_size, n_files, ec2_instance_list[i])
    return None

def get_ec2_instances():
    ec2 = boto3.resource('ec2')        
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    ec2_instance_list = [i.public_ip_address for i in instances]
    return ec2_instance_list

def tar_10ks(ec2_instance_list):
    for ec2_IP in ec2_instance_list:
        ec2_command = "tar -czf 10ks-%s.tar.gz 10k" % ec2_IP
        os_command = "ssh -o UserKnownHostsFile=~/Dropbox/aws/aws_khosts -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
        print os.system(os_command)

def send_to_s3(ec2_instance_list):
    for ec2_IP in ec2_instance_list:
        ec2_command = "aws s3 cp 10ks-%s.tar.gz s3://btcoal" % ec2_IP
        os_command = "ssh -o UserKnownHostsFile=~/Dropbox/aws/aws_khosts -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
        print os.system(os_command)

if __name__ == '__main__':
    ## Spawn EC2 instances
    ec2 = boto3.resource('ec2')
    ec2.create_instances(ImageId=AMI_ID, InstanceType="t2.medium", SecurityGroupIds=[SEC_GROUP_ID], MinCount=1, MaxCount=N_INSTANCES)
    
    time.sleep(120)  # Should be enough time to wait for all instances to get up and running

    ec2_instance_list = get_ec2_instances()

    ## Send each list of URLs to each EC2 instance
    send_urls(ec2_instance_list, FILINGS_URLS)

    ## download urls
    for ec2_IP in ec2_instance_list:
        ec2_command = "<10k/urls.txt xargs -n 1 -P 2 wget -P 10k -q"
        
        os_command = "ssh -o UserKnownHostsFile=~/Dropbox/aws/aws_khosts -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
        print ec2_IP, os.system(os_command)

    #tar_10ks(ec2_instance_list)
    #send_to_s3(ec2_instance_list)
