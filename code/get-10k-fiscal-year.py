#!/usr/bin/env python

## AUTHOR: Reginald Edwards
## CREATED: 4 March 2017
## MODIFIED: 02 June 2017
## DESCRIPTION: Get fiscal year associated with a 10-K by matching line of text in 10-K file that declares the
##   fiscal year

import re
from os import listdir
import time

## Unit tests
fyear_line1 = 'fiscal year ended December 31, 2005'
fyear_line2 = 'fiscal year ended December 31, 2010'
fyear_line3 = 'fiscal year ended December 31, 1995'
fyear_line4 = 'fiscal year ended 12/03/97'
fyear_line5 = 'fiscal year ended 12/03/1997'
fyear_line6 = 'fiscal year ended 12/03/2010'
fyear_line6 = 'fiscal year ended 12/03/10'
fyear_line7 = 'fiscal year ended 12-31-2005'
fyear_line8 = 'fiscal year ended 12-31-05'
fyear_line9 = 'fiscal year ended 12-31-1995'
fyear_line10 = 'fiscal year ended 12-31-95'
fyear_line11 = 'fiscal year ended 12-2005'
fyear_line12 = 'fiscal year ended 12-1995'
fyear_test_lines = [fyear_line1, fyear_line2, fyear_line3,
               fyear_line4, fyear_line5, fyear_line6,
               fyear_line7, fyear_line8, fyear_line9,
               fyear_line10, fyear_line11, fyear_line12]

## Program Global Variables
#slash = '\\'
slash = '/'
_10K_LOC = "/media/reg/607049A4704981B0/compustat-10ks"
#_10K_LOC = "../../data/raw"
METADATA_LOC = "/home/reg/Dropbox/Research/Text Analysis of Filings/metadata"

def get_fyear(contents):
    fyear = 'NA'
    fyear_line = 'NA'

    m = re.search(r'conformed period of report:\s*([0-9]{8})', contents, flags = re.IGNORECASE | re.MULTILINE)
    try:
        fyear_line = m.group()
        fyear = m.group(1)
    except:
        pass
    return fyear[:4]

def get_fyear_2(contents):
    ## Read in contents and find the line in 10-K that describes the fiscal year. Store that line
    ## (100 characters after the mention of the fiscal year) in a dictionary with the file name
    ## as the key.
    find_line_1 = "fiscal year ended"
    find_line_2 = "the year ended"

    fyear_index = -1
    fyear_line = 'NA'
    
    fyear_index = contents.lower().find(find_line_1)
    if fyear_index > -1:
        fyear_line = contents[fyear_index:(fyear_index+100)]
    else:
        fyear_index = contents.lower().find(find_line_2)
        if fyear_index > -1:
            fyear_line = contents[fyear_index:(fyear_index+100)]

    ## Extract the fiscal year from the line containing the fiscal year description.
    fyear_index = -1
    fyear = 'NA'
    
    fyear_index = fyear_line.find('199')
    if fyear_index > -1:
        fyear = fyear_line[fyear_index:(fyear_index+4)]
    else:
        fyear_index = fyear_line.find('200')
        if fyear_index > -1:
            fyear = fyear_line[fyear_index:(fyear_index+4)]
        else:
            fyear_index = fyear_line.find('201')
            if fyear_index > -1:
                fyear = fyear_line[fyear_index:(fyear_index+4)]
            else:
                fyear_index = fyear_line.find('/9')
                if fyear_index > -1:
                    fyear = fyear_line[(fyear_index+1):(fyear_index+3)]
                    fyear = '19'+fyear
                else:
                    fyear_index = fyear_line.find('-9')
                    if fyear_index > -1:
                        fyear = fyear_line[(fyear_index+1):(fyear_index+3)]
                        fyear = '19'+fyear
    return fyear

def print_fyears(fyear_list):
    years = {}
    for l in fyear_list:
        year = l[1]
        if year in years:
                years[year] += 1
        else:
                years[year] = 1
    for year in years:
        print year, years[year]


def write_fyears(fyear_list):
    header = '\t'.join(['filename', 'fyear']) + '\n'
    with open(METADATA_LOC + slash + "10k-fyears.txt", 'w') as outfile:
        outfile.write(header)
        for fyear_line in fyear_list:
            outfile.write('\t'.join(fyear_line) + '\n')

if __name__ == '__main__':
    _10k_list = listdir(_10K_LOC)
    
    fyear_list = []
    
    start_time = time.time()
    for _10k in _10k_list:
        tenk_contents = open(_10K_LOC + slash + _10k, 'r').read()
        fyear = get_fyear(tenk_contents)
        if fyear == 'NA':
            fyear = get_fyear_2(tenk_contents)
        fyear_list.append([_10k, fyear])
    stop_time = time.time() - start_time
    print 'time: %s' % stop_time
    
    print_fyears(fyear_list)
    write_fyears(fyear_list)
