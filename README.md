### AUTHOR Reginald Edwards
### CREATED: 02 June 2017
### MODIFIED: 7 Jan 2019


## DOWNLOADING 10-K FILES FROM EDGAR

### ON LOCAL MACHINE
I. Run "get-urls.py" to get list of relevant URLs and associated metadata.
  1. Download the form.gz files for all year-quarters (1993-2018).

  Unzip each form.gz file.

  Outputs form.gz files into "/index-files" folder with filenames of the form "form-<Year>-QTR<Quarter>/gz"     
    - Each index file is a fixed-width file with lines like [form type, company name, CIK, filing date, url path]

  Prepend "https://www.sec.gov/Archives/" to the "url" field
  
  Combine all data from index files into a master table of filings, tab-delimited. Output "master-index" file.

 
    
  7. Get *JUST* the downloadable URL for each 10-K-type form, which we will request from the EDGAR server
     Outputs "urls.txt" file.
    
  8. create database of URL and associated metadata. Each line of this "database" file is like
    [form type, company name, CIK, filing date, url path] with headers
    "[formtype, companyname, cik, filingdate, url]"
    Outputs "ursl-db.txt".

III. Download 10-Ks
  1. See section on "Download 10-Ks on Local Machine", OR
  2. See section on "Download 10-Ks on AWS"
  
IV. Run "get-10k-fiscal-year.py" to get fiscal year from actual 10-K
   This script reads each 10-K in the "/raw" directory.
   Outputs "10k-fyears.txt" that has header "[filename, fyear]".
   Executes in about 4h21min!!!

V. Run "merge-10k-fiscal-year.R"
    This script merges the fixed fiscal years with the rest of the metadata on the 10-K filings.
    Relies on "compustat-urls-db.txt" and "10k-fyears.txt".
    Outputs "compustat-urls-db-fixedfyear.txt"

VI. Run "sample-10ks.py" to get a representative sample of 10-Ks for testing code



### DOWNLOAD 10-Ks ON AWS
====================================================================================================
This section will use 20 EC2 instances on AWS to download the files. The basic approach is to split
the "urls.txt" file into 20 equal sized chunks, send these chunks to each instance, download the
files, and then move the files to S3.

. Follow set-up procedure in "/aws/aws-configure.txt" for each Ubuntu instance.

. To download 10-Ks onto instances, run "/aws/get-filings.py" on local machine.

. Retrieve downloaded 10-Ks from S3.
  . The script "get-comp-cik-10ks.py" should be stored on each EC2 instance
  . Run "get-comp-cik-10ks-driver.py" on local machine
  
. Unzip downloaded tarballs on local machine: run "unzip-10ks.py"
