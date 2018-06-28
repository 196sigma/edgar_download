import os
files = ['10k-03',
'10k-04.tar.gz',
'10k-05.tar.gz',
'10k-06.tar.gz',
'10k-07.tar.gz',
'10k-08.tar.gz',
'10k-09.tar.gz',
'10k-10.tar.gz',
'10ks-01.tar.gz',
'10ks-02.tar.gz']

i = 1
for f in files:
    if i < 10:
        i = '0'+str(i)
    else:
        i = str(i)
    os_command = "aws s3 mv s3://btcoal/10ks/%s s3://btcoal/10ks/10k-%s.tar.gz" % (f, i)
    print os_command
    print os.system(os_command)
    i = int(i)
    i += 1
