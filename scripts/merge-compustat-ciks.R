## Reginald Edwards
## 02 June 2017
## 02 March 2018
## Reads in a dataset with COMPUSTAT CIKs and associated metadata for downloading filings from EDGAR.
## Filters urls not asoociated with a COMPUSTAT CIK
## TODO:
## - rewrite in python

rm(list=ls())
library('stringr')

DATA_DIR <- "/home/reg/Dropbox/Research/Text Analysis of Filings/download/data"

compustat.ciks <- read.delim(paste(DATA_DIR, "compustat_ciks.txt", sep = '/'))
compustat.ciks$cik <- as.numeric(compustat.ciks$cik)
compustat.ciks$cik <- stringr::str_pad(compustat.ciks$cik, 10, pad = "0")
compustat.ciks.list <- data.frame(cik = unique(compustat.ciks$cik))

urls.db <- read.delim(paste(DATA_DIR,"urls-db.txt",sep='/'), stringsAsFactors = FALSE)
urls.db$cik <- as.character(urls.db$cik)
#urls.db$cik <- toString(urls.db$cik)
urls.db$cik <- stringr::str_pad(urls.db$cik, 10, pad="0")

## Exclude "ammended" type filings
o <- which(urls.db$formtype %in% c('10-K/A', '10-K405/A', '10-KSB/A', '10-KT/A'))
if(length(o)>0) urls.db <- urls.db[-o, ]

X <- merge(compustat.ciks.list, urls.db, by = c('cik'))

outfilename <- paste(DATA_DIR, "compustat-urls-db.txt", sep = "/")
write.table(x=X, file = outfilename, sep="\t", quote=FALSE, row.names = FALSE)

# Write just URLs to file
outfilename <- paste(DATA_DIR, "compustat-urls.txt", sep = "/")
write.table(x=X$url, file = outfilename, sep="\t", quote=FALSE, 
  row.names = FALSE, col.names = FALSE)
