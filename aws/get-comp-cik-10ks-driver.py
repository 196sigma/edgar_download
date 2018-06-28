#!/usr/bin/env python

## Reginald Edwards
## 02 June 2017
## To be run on local machine
## Drives get-comp-cik-10ks.py, which should already be stored on each AWS EC2 Ubuntu instance.
## 

# get-comp-cik-10ks-driver.py
import os
import time
## Get list of S3 files
def get_s3_files():
    os_command = "aws s3 ls s3://redwards-10k > s3_files.txt"
    os.system(os_command)
    with open("s3_files.txt",'r') as infile:
        s3_files_list = [line.strip().split()[-1] for line in infile if line.find("10k")>0]
    return s3_files_list

## spawn 11 ec2 instances
def start_instances(ami_id='', n_instances=2):
    os.system("aws ec2 run-instances --image-id %s --security-group-ids sg-23ab2245 --count %d --instance-type t2.micro --key-name aws-reg-key-1" % (ami_id, n_instances))
    return None
## Get instance ID's, IP addresses
def get_ec2_instances():
    os.system("aws ec2 describe-instances --query \"Reservations[*].Instances[*].PublicIpAddress\" --output=text > ec2-instances-dns.txt")
    ec2_instance_list = open('ec2-instances-dns.txt','r').readlines()

    x=[]
    for i in ec2_instance_list:
        x.append(i.strip('\n').replace('\t',' '))
    y=[]
    for i in x:    
        y.extend(i.split(' '))

    ec2_instance_list = y

    while True:
        try:
            ec2_instance_list.remove('')
        except:
            break
    
    return ec2_instance_list

def send_s3_files(ec2_instance_list, s3_files_list):
	d={}
	s3_files_list_iter = iter(s3_files_list)
	for ec2_IP in ec2_instance_list:
		x=s3_files_list_iter.next()
		aws_command = "aws s3 cp s3://redwards-10k/%s 10k" % x
		os_command = "ssh -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem -f ubuntu@%s \'%s\'" % (ec2_IP, aws_command)
		print os_command
		os.system(os_command)
		d[ec2_IP] = x
	return d

def foo(ec2_instance_list, s3_files_list):
    #s3_files_list_iter = iter(s3_files_list)
    for ec2_IP in ec2_instance_list:
        #x = next(s3_files_list_iter)
        #print x
        #os_command = "ssh -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem -f ubuntu@%s \'rm -rf /home/ubuntu/10k/data && mv /home/ubuntu/data /home/ubuntu/10k/data\'" % ec2_IP
        os_command = "ssh -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem ubuntu@%s \'rm *10k/get*\'" % ec2_IP
        print os_command
        os.system(os_command)
        
        os_command = "scp -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem get-comp-cik-10ks.py ubuntu@%s:10k" % ec2_IP
        print os_command
        os.system(os_command)

def get_compustat_10ks_driver(ec2_instance_list, s3_files_list):
	s3_files_list_iter = iter(s3_files_list)
	for ec2_IP in ec2_instance_list:
		#os_command = "ssh -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem -f ubuntu@%s \'tar -xzf /home/ubuntu/10k/%s\'" % (ec2_IP, s3_files_list_iter.next())
		#print os_command
		#os.system(os_command)
		aws_command = "./10k/get-comp-cik-10ks.py %s" % ec2_IP
		os_command = "ssh -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem -f ubuntu@%s \'%s\'" % (ec2_IP, aws_command)
		print os_command
		os.system(os_command)
	return None

if __name__ == '__main__':
    s3_files_list = get_s3_files()

    print s3_files_list
    
    n_files = len(s3_files_list)

    start_instances('ami-859046e5',10)
    
    ec2_instance_list = get_ec2_instances()
    
    print ec2_instance_list

    ec2_s3_map = send_s3_files(ec2_instance_list, s3_files_list)

    time.sleep(60*60)

    foo(ec2_instance_list, s3_files_list)

    get_compustat_10ks_driver(ec2_instance_list, s3_files_list)

    aws_command='ls -lh 10k'
    for ec2_IP in ec2_instance_list:
		print '###############################  ',ec2_IP,'  ###############################'
		os_command="ssh -o StrictHostKeyChecking=no -i ~/.ssh/aws-reg-key-1.pem ubuntu@%s \'%s\'" % (ec2_IP, aws_command)
		os.system(os_command)
