#!/usr/bin/env python
## This script will enable your local machine to transfer files between remote EC2 instances without
## directing ssh to the private key each time. 
## This is necessary to set up a cluster with EC2 instances

import os
import boto3

PEM_KEY_LOC = '/home/reggie/Dropbox/aws/aws-key.pem'

## Get IP addresses of all running EC2 instances
ec2 = boto3.resource('ec2')        
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
ec2_instance_list = [i.public_ip_address for i in instances]

for instance in ec2_instance_list:
    os.system("scp -o StrictHostKeyChecking=no -i %s ~/.ssh/id_rsa.pub ubuntu@%s:" % (PEM_KEY_LOC, instance))
    os.system("ssh -o StrictHostKeyChecking=no -i %s ubuntu@%s 'cat id_rsa.pub >> ~/.ssh/authorized_keys'" % (PEM_KEY_LOC, instance))
