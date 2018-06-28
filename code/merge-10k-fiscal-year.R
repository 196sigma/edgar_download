rm(list=ls())
library(sas7bdat)

## Reginald Edwards
## 05 June 2017
## Get fiscal year of filings

## Program Data
LOC_10K_DB = "metadata/sample-compustat-urls-db.txt"
LOC_10K_FYEARS = "metadata/10k-fyears.txt"
LOC_COMPUSTAT_CIKS = "~/Dropbox/Research/0_datasets/sample_ciks.sas7bdat"

## Helper functions
## Extract file name of url
get.filename <- function(current.url){
  filename <- unlist(strsplit(current.url, "/"))
  filename <- filename[length(filename)]
  return(filename)
}
get.cik <- function(current.url){
  filename <- unlist(strsplit(current.url, "/"))
  cik <- as.numeric(filename[7])
  return(cik)
}

###################################################################################################

## Load COMPUSTAT dataset with [CIK, fyear, fyear end month]
compustat.ciks <- read.sas7bdat(LOC_COMPUSTAT_CIKS)
cik <- compustat.ciks$cik
cik <- as.numeric(levels(cik))[cik]
compustat.ciks$cik <- cik

## Load dataset with [filename, CIK, filing date]
compustat.urls <- read.delim(LOC_10K_DB, stringsAsFactors = FALSE)
compustat.urls$filename <- unlist(lapply(compustat.urls$url, get.filename))

## Load dataset with [filename, text-imputed fyear]
fyears <- read.delim(LOC_10K_FYEARS, quote="", row.names=NULL, col.names =  c("filename", "fyear1"), stringsAsFactors = FALSE)

## Merge datasets with [filename, text-imputed fiscal year] and [filename, CIK, filingdate]
X <- merge(compustat.urls, fyears, by=c("filename"), all.x = TRUE)
X$fyear1 <- as.numeric(X$fyear1); summary(X$fyear1); table(X$fyear1)

## If month of filingdate is in december then fyear is that year otherwise impute the fyear as the 
## prior year.
## TODO: Refactor using lapply!!!
X$fyear2 <- rep(NA, nrow(X))
for(i in 1:nrow(X)){
  filingdate <- X[i,'filingdate']
  mo <- as.numeric(unlist(strsplit(filingdate,'-'))[2])
  fyear <- unlist(strsplit(filingdate,'-'))[1]
  if(mo > 5){ 
    X[i,'fyear2'] <- as.numeric(fyear)
  }else{
    X[i,'fyear2'] <- as.numeric(fyear)-1
  }
}
summary(X$fyear2); table(X$fyear2)
X[,"fyear.diff"] <- X$fyear1 - X$fyear2; table(X[,"fyear.diff"])
o <-which(is.na(X$fyear.diff))
for(i in 1:10) print(length(which(abs(X[-o,"fyear.diff"]) < i))/nrow(X[-o,]))

## Check correlations for diagnostic/sanity check purposes
cor(X[,c("fyear2", "fyear1")], use="pairwise.complete.obs", method="pearson")
cor(X[,c("fyear2", "fyear1")], use="pairwise.complete.obs", method="kendall")
cor(X[,c("fyear2", "fyear1")], use="pairwise.complete.obs", method="spearman")
## Check outliers
outliers <- which(X[,"fyear.diff"] <= -1)
X1 <- X[outliers, ]
o <- order(X1$fyear.diff)
X1 <- X1[o,]

## Assign filing date-imputed fiscal year to obs with NAs from text-imputed fiscal year
## Assign final fyear and Remove unneccesary fiscal year fields.
## If difference is within two years, go with text-imputed version, otherwise discard observation
o <- which(abs(X$fyear.diff) <= 2 | is.na(X$fyear.diff))
out.df <- X[o,]
out.df$fyear <- ifelse(is.na(out.df$fyear1), out.df$fyear2, out.df$fyear1)
out.df$fyear2 <- NULL
out.df$fyear1 <- NULL
out.df$fyear.diff <- NULL
names(out.df)
summary(out.df$fyear)
plot(table(out.df$fyear))
## Merge into COMPUSTAT dataset
out.df <- merge(out.df, compustat.ciks, by = c("cik", "fyear"))
## Write out data
write.table(x=out.df, file="metadata/sample-compustat-urls-db-fixedfyear.txt", sep="\t", quote=FALSE, row.names = FALSE)
