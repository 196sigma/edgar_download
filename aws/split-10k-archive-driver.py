#!/usr/bin/env python
import os
import boto3
import time
from itertools import cycle

AMI_ID = "ami-8171f2e1"
SEC_GROUP_ID='sg-f9d54281'
N_INSTANCES = 20
PEM_KEY_LOC = '/home/reggie/Dropbox/aws/aws-key.pem'

def get_ec2_instances():
    ec2 = boto3.resource('ec2')        
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    ec2_instance_list = [i.public_ip_address for i in instances]
    return ec2_instance_list

def send_script(f):
    ## Copy main file to each EC2 instance
    file_to_copy = f
    for ec2_IP in ec2_instance_list:
        os_command = 'scp -o StrictHostKeyChecking=no -i %s %s ubuntu@%s:' % (PEM_KEY_LOC, file_to_copy, ec2_IP)
        print os_command
        print os.system(os_command)

def copy_files_from_s3():
    ## Send command to each EC2 instance to copy a tarfile on S3 to itself
    for ec2_IP in instance_tarfile_dict:
        tarfile = instance_tarfile_dict[ec2_IP]
        ec2_command = "aws s3 cp s3://btcoal/10ks/%s ." % tarfile
        os_command = "ssh -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
        print os_command
        print os.system(os_command)

def execute_script(f):
    ## Send command to each EC2 instance to execute script on files
    for ec2_IP in instance_tarfile_dict:
        tarfile = instance_tarfile_dict[ec2_IP]
        ec2_command = "./%s %s" % (f, tarfile)
        os_command = "ssh -o StrictHostKeyChecking=no -i %s -f ubuntu@%s '%s'" % (PEM_KEY_LOC, ec2_IP, ec2_command)
        print os_command
        print os.system(os_command)

if __name__ == '__main__':
    script_name = 'split-10k-archive.py'
    tarfiles = ['10k-01.tar.gz',
    '10k-02.tar.gz',
    '10k-03.tar.gz',
    '10k-04.tar.gz',
    '10k-05.tar.gz',
    '10k-06.tar.gz',
    '10k-07.tar.gz',
    '10k-08.tar.gz',
    '10k-09.tar.gz',
    '10k-10.tar.gz']

    #tarfiles = ['10k-01.tar.gz', '10k-02.tar.gz']

    ## Spawn EC2 instances
    #ec2 = boto3.resource('ec2')
    #ec2.create_instances(ImageId=AMI_ID, InstanceType="t2.medium", SecurityGroupIds=[SEC_GROUP_ID], MinCount=1, MaxCount=N_INSTANCES)

    #time.sleep(120)  # Should be enough time to wait for all instances to get up and running

    ec2_instance_list = get_ec2_instances()
    for x in ec2_instance_list:
        print x
    send_script(script_name)

    ## Map each tar file to its own EC2 instance and store the mapping in in a dictionary object
    instance_tarfile_dict = {}
    instance_tarfile_dict = instance_tarfile_dict.fromkeys(ec2_instance_list)
    for k in instance_tarfile_dict:
        instance_tarfile_dict[k] = ''
    tarfiles_iter = iter(tarfiles)
    pool = cycle(instance_tarfile_dict.keys())
    for x in tarfiles_iter:
        k = pool.next()
        instance_tarfile_dict[k] = x
    for k in instance_tarfile_dict:
        print k, '\t', instance_tarfile_dict[k]
    copy_files_from_s3()
    #execute_script(script_name)
