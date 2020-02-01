### AUTHOR Reginald Edwards
### CREATED: 02 June 2017
### MODIFIED: 7 Jan 2019

## About
This repo is a collection of notebooks and scripts for downloading corporate filings from the United States Securities and Exchange Commission EDGAR database.

### Notebooks
Download XBRL Filings v2
    * Download Financial Statements and Notes Datasets from EDGAR.ipynb
    * Compile Subs from FSANDS.ipynb
    
Download 10-K's from EDGAR

## DOWNLOADING 10-K FILES FROM EDGAR

The basis for downloading company filings are the SEC index files. The index files are stored at https://www.sec.gov/Archives/edgar/full-index/. The structure of the SEC index files stored on their EDGAR server is as follows.
* There is a folder for every year
* Within each year folder there is a folder for every quarter ("QTR1", "QTR2",etc)
* Within each quarter folder there are many files that describe the submissions to the SEC during that year-quarter. The most useful is the master file (master.gz).