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

_10ks = get_filings_from_index('D:/edgar-master-index', '10K')

urls = [line[-1] for line in _10ks]
print(len(urls))

start = time.time()
results = ThreadPool(N_PROC).imap_unordered(download_filing_from_url, urls)
for path in results:
    print(path)
exec_time = time.time() - start