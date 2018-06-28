#!/usr/bin/env python

# parse_xbrl.py
from xml.etree import ElementTree as ET
import re
from BeautifulSoup import BeautifulSoup
import os
import sys
import pickle


## INPUTS:
##  - xml_filename: (String)
##  - xml_metadata_filename: (String)
##  - outfile_name: (String)
## OUTPUTS:
##  - outfile_name: (String)
## SIDE-EFFECTS: 
##  - Creates a TDF with file name specified in outfile_name, which contains...
def get_metadata(xml_filename, xml_metadata_filename, outfile_name):
    ## find record of associated .xml file in master file
    ## append 10-K XBRL section title
    ## write to database file
    
    return outfile_name

## INPUTS:
##  - INPUT_DIR: (String)
##  - OUTPUT_DIR: (String)
##  - xml_files_list: (List)
## OUTPUTS:
##  - parse_success: (Boolean)
## SIDE-EFFECTS: 
##  - creates a dictionary of parsed XML file information (metadata)
##  - creates text files of parsed XBRL files
##  - creates a TDF of information of files that were not parsed
def parse_xbrl_l(INPUT_DIR, OUTPUT_DIR, xml_files_list, xbrl_section):
    parse_success = False
    parsed_db = {}    
    ## load instance metadata db
    instance_db = pickle.load(open("/home/reg/Dropbox/Research/Text Analysis of Filings/xbrl/data/instance_db", "rb"))
    errors = open('/home/reg/Dropbox/Research/Text Analysis of Filings/xbrl/data/parse-errors.txt','w')
    errors_list = []
    notparsed_list = []
    notparsed = open('/home/reg/Dropbox/Research/Text Analysis of Filings/xbrl/data/notparsed.txt','w')
    
    for xml_file in xml_files_list:
        output_name = xml_file.replace('.xml','.txt')

        ## check if XML file has already been parsed
        try:
            ## Tell Python to ignore namespaces when parsing
            it = ET.iterparse(INPUT_DIR + '/' + xml_file)
            for _, el in it:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
            root = it.root
            data=root.find(xbrl_section)

            if data is not None:
                #print "found data"
                text = data.text

                ## Remove HTML tables and tags
                soup = BeautifulSoup(text)
                for table_tag in soup.findAll('table'):
                    table_tag.extract()
                text = soup.text

                ## Transform character entity references
                text = re.sub('&#160;', ' ', text)
                text = re.sub('&#8211;', ' ', text)
                
                #print output_name
                with open(OUTPUT_DIR+'/'+output_name,'w') as outfile:
                    outfile.write(text)
                    
                ## Updated parsed XBRL XML metadata dictionary
                instance = xml_file
                cik, adsh, name, form, fy, period, sub_url = [var for var in instance_db[instance]]
                metadata = (cik, adsh, name, form, fy, period, sub_url, xbrl_section)
                parsed_db[output_name] = metadata
                parse_success = True
                
            else:
                notparsed_list.append(xml_file+'\n')
        except:
            e = sys.exc_info()[0]
            errors_list.append(xml_file + '\t' + str(e)+'\n')
            notparsed_list.append(xml_file+'\n')

    errors.writelines(errors_list)
    errors.close()
    notparsed.writelines(notparsed_list)
    notparsed.close()
    ## Serialize database12
    pickle.dump( parsed_db, open( OUTPUT_DIR + '/parsed_db', "wb" ) )
    
    return parse_success

## INPUTS:
##  - INPUT_DIR: (String)
##  - OUTPUT_DIR: (String)
##  - xml_files_list: (List)
## OUTPUTS:
##  - parse_success: (Boolean)
## SIDE-EFFECTS: 
##  - creates a dictionary of parsed XML file information (metadata)
##  - creates text files of parsed XBRL files
##  - creates a TDF of information of files that were not parsed
def parse_driver(INPUT_DIR, OUTPUT_DIR, xml_files_list, xbrl_section):
    try:
        parsed_db = pickle.load(open(OUTPUT_DIR + '/parsed_db', 'rb'))
    except:
        parsed_db = {}
        
    for xml_file in xml_file_list:
        output_name = xml_file.replace('.xml','.txt')
        if output_name in parsed_db:
            print 'already parsed, moving on...'
        else:
            print 'new file %s to parse' % xml_file
            parse_xbrl(INPUT_DIR, OUTPUT_DIR, xml_file, xbrl_section)
    
def parse_xbrl(INPUT_DIR, OUTPUT_DIR, xml_file, xbrl_section):
    parse_success = False
    
    try:
        parsed_db = pickle.load(open(OUTPUT_DIR + '/parsed_db', 'rb'))
    except:
        parsed_db = {}
        
    ## load instance metadata db
    instance_db = pickle.load(open("/home/reg/Dropbox/Research/Text Analysis of Filings/xbrl/data/instance_db", "rb"))
    errors = open('/home/reg/Dropbox/Research/Text Analysis of Filings/xbrl/data/parse-errors.txt','a')
    errors_list = []
    notparsed_list = []
    notparsed = open('/home/reg/Dropbox/Research/Text Analysis of Filings/xbrl/data/notparsed.txt','a')
    
    output_name = xml_file.replace('.xml','.txt')

    ## check if XML file has already been parsed
    try:
        ## Tell Python to ignore namespaces when parsing
        it = ET.iterparse(INPUT_DIR + '/' + xml_file)
        for _, el in it:
            el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
        root = it.root
        data=root.find(xbrl_section)

        if data is not None:
            #print "found data"
            text = data.text

            ## Remove HTML tables and tags
            soup = BeautifulSoup(text)
            for table_tag in soup.findAll('table'):
                table_tag.extract()
            text = soup.text

            ## Transform character entity references
            text = re.sub('&#160;', ' ', text)
            text = re.sub('&#8211;', ' ', text)
            
            with open(OUTPUT_DIR+'/'+output_name,'w') as outfile:
                outfile.write(text)
                
            ## Updated parsed XBRL XML metadata dictionary
            instance = xml_file
            cik, adsh, name, form, fy, period, sub_url = [var for var in instance_db[instance]]
            metadata = (cik, adsh, name, form, fy, period, sub_url, xbrl_section)
            parsed_db[output_name] = metadata
            parse_success = True
            
        else:
            notparsed_list.append(xml_file+'\n')
    except:
        e = sys.exc_info()[0]
        errors_list.append(xml_file + '\t' + str(e)+'\n')
        notparsed_list.append(xml_file+'\n')

    errors.writelines(errors_list)
    errors.close()
    notparsed.writelines(notparsed_list)
    notparsed.close()
    ## Serialize database12
    pickle.dump( parsed_db, open( OUTPUT_DIR + '/parsed_db', "wb" ) )
    
    return parse_success

## TODO Implement a function to try a hierarchy of XBRL tags
## INPUTS:
##  - INPUT_DIR: (String)
##  - OUTPUT_DIR: (String)
##  - xml_files_list: (List)
##  - xbrl_section_list: (List) XBRL section tags in decreasing order of parsing priority
## OUTPUTS:
##  - 
## SIDE-EFFECTS: 
##  - creates a dictionary of parsed XML file information (metadata)
##  - creates text files of parsed XBRL files
##  - creates a TDF of information of files that were not parsed
def multipass_parse_xbrl(INPUT_DIR, OUTPUT_DIR, xml_files_list, xbrl_section_list):
    n_passes = len(xbrl_section_list)
    
    try:
        parsed_db = pickle.load(open(OUTPUT_DIR + '/parsed_db', 'rb'))
        print 'parsed database loaded'
    except:
        parsed_db = {}
    
    n_parsed = len(parsed_db)    
    
    for xml_file in xml_files_list:
        #print xml_file
        output_name = xml_file.replace('.xml','.txt')
        if output_name in parsed_db:
            pass
        else:
            i = 0
            #print 'new file %s to parse' % xml_file
            #print 'trying xbrl tag level ' + str(i) 
            xbrl_section = xbrl_section_list[i]
            parse_success = parse_xbrl(INPUT_DIR, OUTPUT_DIR, xml_file, xbrl_section)
            while i < (n_passes - 1):
                if not parse_success:
                    #print 'trying xbrl tag level ' + str(i)
                    i += 1
                    xbrl_section = xbrl_section_list[i]
                    parse_success = parse_xbrl(INPUT_DIR, OUTPUT_DIR, xml_file, xbrl_section)                        
                else:
                    n_parsed += 1
                    print 'succeeded parsing %s at level %f' % (xml_file, i)
                    break
            print str(n_parsed) + ' parsed'
    print str(n_parsed) + ' files parsed'
    return n_parsed

if __name__ == '__main__':
    INPUT_DIR = '/media/reg/607049A4704981B0/temp'
    
    OUTPUT_DIR = '/media/reg/607049A4704981B0/SignificantAccountingPoliciesTextBlock'
    
    xbrl_section = 'SignificantAccountingPoliciesTextBlock'
    """
    xbrl_section_list = ['SignificantAccountingPoliciesTextBlock', 
                         'BasisOfPresentationAndSignificantAccountingPoliciesTextBlock',
                         'BusinessDescriptionAndAccountingPoliciesTextBlock',
                         'NewAccountingPronouncementsPolicyPolicyTextBlock', 
                         'OrganizationConsolidationAndPresentationOfFinancialStatementsDisclosureAndSignificantAccountingPoliciesTextBlock',
                         'OrganizationConsolidationAndPresentationOfFinancialStatementsDisclosureTextBlock',
                         'ScheduleOfNewAccountingPronouncementsAndChangesInAccountingPrinciplesTextBlock']
    """
    xbrl_section_list = ['SignificantAccountingPoliciesTextBlock', 
                        'BasisOfPresentationAndSignificantAccountingPoliciesTextBlock',
                        'BusinessDescriptionAndAccountingPoliciesTextBlock',
                        'OrganizationConsolidationAndPresentationOfFinancialStatementsDisclosureAndSignificantAccountingPoliciesTextBlock',
                        'NewAccountingPronouncementsPolicyPolicyTextBlock']
    
    ## TODO: Pass data directory from standard-in
    xml_files_list = os.listdir(INPUT_DIR)
    ## remove non-xml files
    for f in xml_files_list:
        if f.find('.xml') < 0 :
            xml_files_list.remove(f)
    
    #parse_xbrl(INPUT_DIR, OUTPUT_DIR, xml_files_list, xbrl_section)

    multipass_parse_xbrl(INPUT_DIR, OUTPUT_DIR, xml_files_list, xbrl_section_list)

    #parsed_db = pickle.load(open("/home/reg/Dropbox/Research/Text Analysis of Filings/xbrl/data/SignificantAccountingPoliciesTextBlock/parsed_db", "rb"))
