## Reginald Edwards
## 2 June, 2017
## This code gets CIKs from COMPUSTAT and associated metadata. These CIKs are later used for downloading filings from EDGAR.
library(RPostgres)
wrds <- dbConnect(Postgres(), 
                  host='wrds-pgdata.wharton.upenn.edu',
                  port=9737,
                  user='reggie09',
                  password='gbHjz5FV',
                  sslmode='require',
                  dbname='wrds')

res <- dbSendQuery(wrds, 
  "SELECT gvkey, fyear, fyr, datadate, cik, sich, prcc_f, seq, at, sale, conm
  from comp.funda where indfmt = 'INDL' 
  and datafmt = 'STD'
  and popsrc = 'D'
  and consol = 'C'
  and final = 'Y'
  and fyear <= 2018
  and fyear >= 1991
  and CIK IS NOT NULL")
X <- dbFetch(res)
dbClearResult(res)
#save(comp.funda, file = '0_datasets/comp_funda.RData')

libname_home <- '/home/reg/Dropbox/Research/0_datasets'
libname_mydata <- '/home/reg/Dropbox/Research/Text Analysis of Filings/download/data'

#/*Exclude financial firms*/
o <- which(X$sich %in% seq(6000:6999))
if(length(o) > 0) X <- X[-o, ]

# Price- and size-based exclusions
o <- which(X$prcc_f < 2 | X$seq <= 0 | X$at <= 1 | X$sale <= 0)
if(length(o) > 0) X <- X[-o, ]  

# Exclude holding companies, ADRs, and limited partnerships: 
# identify which company name contains the word
# "Holdings Group", "Hldgs", "Grp", "ADR", "LTD", or "LP" */
is.holding <- function(x) return(grepl("HOLDINGS| HLDGS| -ADR| -LP| LTD| GRP", 
  x, ignore.case = TRUE))

X$holding <- unlist(lapply(X$conm, is.holding))
X <- X[X$holding == FALSE, ]
o <- which(duplicated(X[c('gvkey', 'fyear')]) == TRUE)
if(length(o) > 0) X <- X[-o, ]

## Get two-digit SIC code
X$sic2 <- trunc(X$sich/100)

outfilename <- paste(libname_mydata, "compustat_ciks.txt", sep = '/')
write.table(X, file = outfilename, sep = '\t')
