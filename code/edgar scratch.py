
# coding: utf-8

# In[1]:


import urllib
import gzip
import re
import shutil
import os
import pandas as pd
import requests


# In[2]:



MIN_YEAR = 1991
MAX_YEAR = 2017
EXT_DIR = "/media/reg/607049A4704981B0"
## windows
EXT_DIR = "D:"
HOME_DIR = "/home/reg/Dropbox/Research/Text Analysis of Filings/code/download"
DATA_DIR = HOME_DIR + "/data"
METADATA_DIR = HOME_DIR + "/data"
TEMP_DIR = '/tmp'
TEMP_DIR = 'C:/tmp'


# In[3]:


## Download form.idx files.
## The .idx files are index files that have the information we want and the .gz files are compressed
## versions of those.
## There is a form.gz file for each year-quarter.
def download_index_files(min_year, max_year, min_quarter = 1, max_quarter = 4, index_file_dir = ""):
    for year in range(min_year, max_year+1):
        for quarter in range(min_quarter, max_quarter+1):
            print( "Downloading index file for %s, Q%s" % (year, quarter))
            try:
                index_file_url = "https://www.sec.gov/Archives/edgar/full-index/{}/QTR{}/form.gz".format(year, quarter)
                index_file_temp_path = os.path.join(TEMP_DIR, "form-{}-QTR{}.gz".format(year, quarter))
                urllib.request.urlretrieve(index_file_url, index_file_temp_path)
            except:
                print( "ERROR: Download failed!")
                
            ## extract
            index_file_filename = os.path.join(index_file_dir, "form-{}-QTR{}".format(year, quarter))
            try:
                with gzip.open(index_file_temp_path, 'rb') as infile:
                    with open(index_file_filename, 'wb') as outfile:
                        shutil.copyfileobj(infile, outfile)
            except:
                print("ERROR: Could not extract!")
    return 0


# In[4]:


#download_index_files(1991, 2016, 1, 4, os.path.join(EXT_DIR, "edgar-index-files"))


# In[4]:


#Create table of formtype, companyname, cik, filename, url that will be updated every quarter
## clean master index file
def clean_master_index_file(master_index_file):
    url_base = "https://www.sec.gov/Archives/"
    contents = []
    if type(master_index_file) is str:
        try:
            with open(master_index_file, "r") as infile:
                for current_line in infile:
                    current_line = current_line.strip().split()
                    n = len(current_line)
                    form_type = current_line[0]
                    filing_url = current_line[-1]
                    filing_date = current_line[n-2]
                    cik = current_line[n-3]
                    company_name = ' '.join(current_line[1:(n-4)])
                    out_line = '|'.join([form_type, company_name, cik, filing_date, url_base + filing_url]) + '\n'
                    contents.append(out_line)
        except:
            print( "WARNING: No file to open!")
    elif type(master_index_file) is list:
        for current_line in master_index_file:
            current_line = current_line.strip().split()
            n = len(current_line)
            form_type = current_line[0]
            filing_url = current_line[-1]
            filing_date = current_line[n-2]
            cik = current_line[n-3]
            company_name = ' '.join(current_line[1:(n-4)])
            out_line = '|'.join([form_type, company_name, cik, filing_date, url_base + filing_url]) + '\n'
            contents.append(out_line)
    return contents

def remove_index_header(index_file):
    with open(index_file, "r") as infile:
        contents = infile.readlines()
    return contents[10:]

def combine_index_files(filename, index_file_dir):
    header = "|".join(["form_type", "company_name", "cik", "filing_date", "url"])+"\n"
    with open(filename, "w") as outfile:
        outfile.writelines(header)
    for index_file in os.listdir(index_file_dir):
        contents = remove_index_header(os.path.join(index_file_dir, index_file))
        contents = clean_master_index_file(contents)
        with open(filename, "a") as outfile:
            outfile.writelines(contents)
            
def append_index_files(master_index_file, index_file):
    contents = remove_index_header(index_file)
    contents = clean_master_index_file(contents)
    with open(master_index_filename, "a") as outfile:
        outfile.writelines(contents)


# In[ ]:


combine_index_files("D:/edgar-master-index", "D:/edgar-index-files/")


# In[5]:


## Get all 10-K type filings
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


# In[ ]:


i=0
master = []
with open("D:/edgar-master-index", "r") as infile:
    header = next(infile).strip().split("|")
    while i < 10000:
        line = next(infile)
        line = line.strip().split("|")
        master.append(line)
        i += 1
master = pd.DataFrame(master)
master.columns = header
master.head()


# In[ ]:


master.form_type.value_counts()/master.shape[0]


# In[11]:


import requests
import os
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import time
N_PROC = cpu_count()

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
        try:
            #time.sleep(.1)
            urllib.request.urlretrieve(filing_url, filename)
            status = 0
            #print("Downloaded successfully {} to {}".format(filing_url, filename))
        except:
            print("could not download{}".format(filing_url))
    return status


# In[7]:


_10ks = get_filings_from_index('D:/edgar-master-index', '10K')


# In[8]:


urls = [line[-1] for line in _10ks]
len(urls)


# In[12]:


start = time.time()
results = ThreadPool(N_PROC).imap_unordered(download_filing_from_url, urls)
for path in results:
    print(path)
exec_time = time.time() - start


# In[ ]:


exec_time

