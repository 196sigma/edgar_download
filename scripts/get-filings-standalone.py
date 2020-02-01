import urllib2

MIN_YEAR = 1991
MAX_YEAR = 2017
EXT_DIR = "/media/reg/607049A4704981B0"
HOME_DIR = "/home/reg/Dropbox/Research/Text Analysis of Filings/code/download"
METADATA_DIR = "/home/reg/Dropbox/Research/Text Analysis of Filings/code/download/data"

url_list = [x.strip() for x in open(METADATA_DIR + '/sample-compustat-urls.txt')]

## Get URL portion and form full downloadable link
for x in url_list:
    outname = x.split('/')[-1]
    u = urllib2.urlopen(x)
    with open(EXT_DIR + '/sample-10ks/' + outname, 'w') as outfile:
        outfile.write(u.read())
    #urllib.urlretrieve(x, DATA_DIR + '/sample-10ks/' + outname)
