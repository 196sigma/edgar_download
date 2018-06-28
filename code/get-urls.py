#!/usr/bin/env python

## AUTHOR: Reginald Edwards
## CREATED ON: 2 February, 2017
## LAST MODIFIED: 15 February, 2017
## DESCRIPTION: This script downloads the list of filings from the SEC EDGAR webiste. It outputs a
##              tab-delimited file listing all 10-K type filings from 1991-2017 ("urls_db.txt").
## TODO:
## - more helpful/descriptive print statements in functions
## - separate metadata, data, and code into proper directories

import urllib
import gzip
import re

MIN_YEAR = 1991
MAX_YEAR = 2017
EXT_DIR = "/media/reg/607049A4704981B0"
HOME_DIR = "/home/reg/Dropbox/Research/Text Analysis of Filings/code/download"
DATA_DIR = HOME_DIR + "/data"
METADATA_DIR = HOME_DIR + "/data"

## Download form.idx files.
## The .idx files are index files that have the information we want and the .gz files are compressed
## versions of those.
## There is a form.gz file for each year-quarter.
def download_index_files():
    for YYYY in range(MIN_YEAR, MAX_YEAR+1):
        for QTR in range(1,5):
            print "Downloading index file for %s, Q%s" % (YYYY, QTR)
            try:
                urllib.urlretrieve("https://www.sec.gov/Archives/edgar/full-index/%s/QTR%s/form.gz" % (YYYY, QTR), "%s/sec-downloads/form-%s-QTR%s.gz" % (EXT_DIR, YYYY, QTR))
            except:
                print "WARNING: Download failed!"
    return 0

## Unzip
def unzip_index_files():
    for YYYY in range(MIN_YEAR, MAX_YEAR+1):
        for QTR in range(1,5):
            path_to_file = "%s/sec-downloads/form-%s-QTR%s.gz" % (EXT_DIR, YYYY, QTR)
            path_to_destination = "%s/sec-company-index-files/form-%s-QTR%s" % (EXT_DIR, YYYY, QTR)
            print "unzipping file %s" % path_to_file

            try:
                with gzip.open(path_to_file, 'rb') as infile:
                    with open(path_to_destination, 'wb') as outfile:
                        for line in infile:
                            outfile.write(line)
            except:
                print "WARNING: Unzip failed!"

    print "All files unzipped!"
    return 0

## Get only 10-K type filings from each form index files
## Each index file contains a line like [form type, company name, CIK, filing date, url path]
## Combine all entries for all quarters of a given year into one file per year
def extract_10k_lines():
    total_lines = 0
    for YYYY in range(MIN_YEAR, MAX_YEAR+1):
        outlines = []
        for QTR in range(1,5):
            ## Extract 10-K type files
            try:
                with open("%s/sec-company-index-files/form-%s-QTR%s" % (EXT_DIR, YYYY, QTR), 'r') as infile:
                    for line in infile:
                        if re.search(r'^10-K', line):
                            outlines.append(line)                    
            except:
                print "WARNING: No file to read!"
                    
        print "Writing %s 10-K lines" % YYYY
        
        with open("%s/sec-company-index-files-combined/form-%s-10ks.txt" % (EXT_DIR, YYYY),'w') as outfile:
            outfile.writelines(outlines)
            total_lines += len(outlines)
            print "%s 10-K lines extracted" % len(outlines)
    print "%s 10-K lines extracted" % total_lines
    return 0

## Prepend URL domain ("url_base") to URL path of filing
## Convert to tab-delimited file format
## TODO:
##    - Refactor based on actual column limits.
##    - Change "/output" folder to something more descriptive
def convert_tdf():
    total_lines = 0
    header = '\t'.join(['formtype', 'companyname', 'cik','filingdate','url']) + '\n'
    url_base = "https://www.sec.gov/Archives/"
    for YYYY in range(MIN_YEAR, MAX_YEAR+1):
        print "Converting year %s to TDF" % YYYY
        outline_list = []
        try:
            with open("%s/sec-company-index-files-combined/form-%s-10ks.txt" % (EXT_DIR, YYYY), "r") as infile:
                for currentLine in infile:
                    currentLine = currentLine.split()
                    n = len(currentLine)
                    formType = currentLine[0]
                    filingURL = currentLine[-1]
                    filingDate = currentLine[n-2]
                    CIK = currentLine[n-3]
                    companyName = ' '.join(currentLine[1:(n-4)])
                    outLine = '\t'.join([formType, companyName, CIK, filingDate, url_base + filingURL]) + '\n'
                    outline_list.append(outLine)
        except:
            print "WARNING: No file to open!"
        with open("%s/output/form-%s-10ks-tdf.txt" % (DATA_DIR, YYYY), "w") as outfile:
            print "Writing to tdf file for year %s" % YYYY
            outfile.write(header)
            outfile.writelines(outline_list)
            print "%s files converted to TDF" % len(outline_list)
            total_lines += len(outline_list)
    print "%s files converted to TDF" % total_lines
    return 0

## Combine all years' 10-K submissions data
def combine():
    header = '\t'.join(['formtype', 'companyname', 'cik','filingdate','url']) + '\n'
    print "Combining all years' 10-K submissions data"
    with open("%s/all-10k-submissions.txt" % METADATA_DIR,'w') as outfile:
        outfile.write(header)
        
    with open("%s/all-10k-submissions.txt" % METADATA_DIR,'a') as outfile:
        for YYYY in range(MIN_YEAR, MAX_YEAR+1):
            with open("%s/output/form-%s-10ks-tdf.txt" % (DATA_DIR, YYYY), 'r') as infile:
                outfile.writelines(infile.readlines()[1:])  ## skip header
    print "All years' data combined"
    return 0

## Get URL portion and form full downloadable link
def get_urls(outfilename):
    url_index = 4
    outlines = []
    
    with open("%s/all-10k-submissions.txt" % METADATA_DIR, 'r') as infile:
        infile.next()
        for line in infile:
            line = line.strip().split('\t')
            url = line[url_index]
            outlines.append(url + '\n')
            
    with open("%s" % outfilename,'w') as outfile:
        outfile.writelines(outlines)
        
    print "%s URLs found" % len(outlines)

def make_urls_db(outfilename):
    
    outlines = []
    
    ## Make a URLs database with meta-information
    with open("%s/all-10k-submissions.txt" % METADATA_DIR, 'r') as infile:
        header = infile.next()
        header = header.strip().split('\t')
        cik_index = header.index('cik')
        companyname_index = header.index('companyname')
        url_index = header.index('url')
        filingdate_index = header.index('filingdate')
        formtype_index = header.index('formtype')
        
        for line in infile:
            line = line.strip()
            line = line.split('\t')
            cik = line[cik_index]
            companyname = line[companyname_index]
            url = line[url_index]
            filingdate = line[filingdate_index]
            formtype = line[formtype_index]

            line = '\t'.join([formtype, companyname, cik, filingdate, url]) + '\n'
            outlines.append(line)
    
    with open("%s" % outfilename, 'w') as outfile:
        outfile.write('\t'.join(header)+'\n')
        outfile.writelines(outlines)
        
    return 0


if __name__ == '__main__':
    header = '\t'.join(['formtype', 'companyname', 'cik','filingdate','url']) + '\n'
    #download_index_files()
    #unzip_index_files()
    #extract_10k_lines()
    #convert_tdf()
    #combine()
    get_urls(METADATA_DIR + "/urls.txt")
    make_urls_db(METADATA_DIR + "/urls-db.txt")
