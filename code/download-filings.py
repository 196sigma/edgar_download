import requests
import os
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import time
import re
import pickle
import urllib
N_PROC = cpu_count()
SLEEP_TIME = 1
## Download filings
output_dir ="D:/10k"
def download_filing_from_url(filing_url):
    status = -1
    filename = filing_url.split("/")[-1]
    filename = os.path.join(output_dir, filename)
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("Directory " , output_dir ,  " Created ")

    if not os.path.isfile(filename):
        time.sleep(SLEEP_TIME)
        status = urllib.request.urlretrieve(filing_url, filename)
    return status
"""
        try:
            time.sleep(.1)
            status = urllib.request.urlretrieve(filing_url, filename)
            #print("Downloaded successfully {} to {}".format(filing_url, filename))
        except:
            print("could not download{}".format(filing_url))
"""
def get_filings_from_index(master_index_file, filing_type = '10K'):
    filings = []
    if filing_type == '10K':
        with open(master_index_file, "r") as infile:
            for line in infile:
                line = line.strip().split("|")
                form_type = line[0]
                if re.search(r'^10-K', form_type):
                    filings.append(line)
    elif filing_type == '8K':
        with open(master_index_file, "r") as infile:
            for line in infile:
                line = line.strip().split("|")
                form_type = line[0]
                if re.search(r'^8-K', form_type):
                    filings.append(line)
    elif filing_type == '13F':
        with open(master_index_file, "r") as infile:
            for line in infile:
                line = line.strip().split("|")
                form_type = line[0]
                if re.search(r'^13F', form_type):
                    filings.append(line)

    return filings

def run():
    if not os.path.isfile('10ks'):
        _10ks = get_filings_from_index('D:/edgar-master-index', '10K')
        with open('10ks', 'wb') as outfile:
            pickle.dump(_10ks, outfile)
    else:
        with open('10ks','rb') as infile:
            _10ks = pickle.load(infile)
    urls = [line[-1] for line in _10ks]
    print(len(urls))

    start = time.time()
    results = ThreadPool(N_PROC).imap_unordered(download_filing_from_url, urls)
    for path in results:
        print(path)
    exec_time = time.time() - start
    print(exec_time)

def move_files():
    files = os.listdir(output_dir)
    files = [f for f in files if f.find('.txt') > -1]
    for f in files:
        try:
            year = f.split('-')[1]
            os_command = "mv {} {}/".format(os.path.join(output_dir, f), os.path.join(output_dir, year))
            if not os.path.exists(os.path.join(output_dir, year)):
                os.mkdir(os.path.join(output_dir,year))
            os.system(os_command)
        except:
            print("Error, could not move file")

files = os.listdir(output_dir)
files = [f for f in files if f.find('.txt') > -1]
def move_file(f):
    try:
        year = f.split('-')[1]
        os_command = "mv {} {}/".format(os.path.join(output_dir, f), os.path.join(output_dir, year))
        if not os.path.exists(os.path.join(output_dir, year)):
            os.mkdir(os.path.join(output_dir,year))
        os.system(os_command)
    except:
        print("Error, could not move file")

results = ThreadPool(N_PROC).imap_unordered(move_file, files)
for path in results:
    print(path)
