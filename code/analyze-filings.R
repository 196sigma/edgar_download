## Analyze filings
# 02/02/2017
## TODO:
##  1. replace table() functions with aggregate() calls
rm(list=ls())

## Read a given year's 10-K Filings
X <- read.csv("download-filings/all-10k-submissions.txt", stringsAsFactors=FALSE, sep='\t')
X$filingdate <- as.Date(X$filingdate)
X$filingyear <- as.numeric(format(X$filingdate, "%Y"))
table(X[,"formtype"])
table(X[,"filingyear"])

###################################################################################################
## Count filings by type by year
A <- as.data.frame.matrix(table(X[,c("filingyear", "formtype")]))

## Clean formtype field
x <- c()
for(a in names(A)) x <- c(x, paste('x', gsub('-|/','',a),  sep=''))
names(A) <- x

A$all <- rowSums(A, na.rm=TRUE)
A$filingyear <- rownames(A)
filings.by.date <- data.frame(filingyear = A$filingyear, all = A$all, A[,1:(ncol(A)-2)] )
filings.by.date$filingyear <- as.character(filings.by.date$filingyear)
rownames(filings.by.date) <- NULL
jpeg(filename = '10k-filings-by-year.jpeg', width=(480*1.25), height = 480, quality = 100)
plot(x=filings.by.date$filingyear, filings.by.date$all, xaxs='i', lwd=2, type='l', col='grey60', 
     ylim=c(0,16000), xlab="Filing Year", ylab="No. Filings")
points(filings.by.date$filingyear, filings.by.date$x10K, lwd=2, type='l', col='red')
points(filings.by.date$filingyear, filings.by.date$x10KA, lwd=2, type='l', col='orange')
points(filings.by.date$filingyear, filings.by.date$x10K405, lwd=2, type='l', col='blue')
points(filings.by.date$filingyear, filings.by.date$x10K405A, lwd=2, type='l', col='green')
points(filings.by.date$filingyear, filings.by.date$x10KT, lwd=2, type='l', col='yellow')
points(filings.by.date$filingyear, filings.by.date$x10KTA, lwd=2, type='l', col='purple')

legend(x=1996, y=15500, lty=1, lwd=2, ncol=4, 
       legend=c("All", "10-K", "10-K/A", "10-K405", "10-K405/A", "10-KT", "10-KT/A"), 
       col=c('grey60', 'red', 'orange', 'blue', 'green', 'yellow', 'purple'))
dev.off()

#################################
## Count filings by type by day
o <- which(X$filingyear == 2016)
A <- as.data.frame.matrix(table(X[o,c("filingdate", "formtype")]))

## Clean formtype field
x <- c()
for(a in names(A)) x <- c(x, paste('x', gsub('-|/','',a),  sep=''))
names(A) <- x

A$all <- rowSums(A, na.rm=TRUE)
A$filingdate <- rownames(A)
A$filingdate <- as.Date(A$filingdate)
filings.by.date <- data.frame(filingdate = A$filingdate, all = A$all, A[,1:(ncol(A)-2)] )
rownames(filings.by.date) <- NULL

plot(filings.by.date$filingdate, filings.by.date$all, xaxs='i', ylim=c(0,1000), 
     type='l', col='grey60')
points(filings.by.date$filingdate, filings.by.date$x10K, type='l', col='red')
points(filings.by.date$filingdate, filings.by.date$x10KA, type='l', col='orange')
points(filings.by.date$filingdate, filings.by.date$x10K405, type='l', col='blue')
points(filings.by.date$filingdate, filings.by.date$x10K405A, type='l', col='green')
points(filings.by.date$filingdate, filings.by.date$x10KT, type='l', col='yellow')
points(filings.by.date$filingdate, filings.by.date$x10KTA, type='l', col='purple')

legend(x='topleft', bty='n', lty=1, lwd=2, ncol=5, 
       legend=c("All", "10-K", "10-K/A", "10-K405", "10-K405/A", "10-KT", "10-KT/A"), 
       col=c('grey60', 'red', 'orange', 'blue', 'green', 'yellow', 'purple'))


###################################################################################################
## Count all CIKs by year
ciks <- as.data.frame.matrix(table(X[,c("filingyear", "cik")]))

A <- aggregate(data=X, cik ~ filingyear, function(x) length(x))

## Count unique CIKs by year
A1 <- aggregate(data=X, cik ~ filingyear, function(x) length(unique(x)))

## plot
barplot(A$n.cik, names.arg=A$filingyear, xaxs='i', space=1, ylim=c(0,15000), col='blue', 
        border=NA, ylab="No. CIKs", xlab="Year")
abline(h=seq(0, 15000, 2000), v=seq(1,46, 2), col='grey60', lwd=1)
barplot(A$n.cik, names.arg=A$filingyear, xaxs='i', space=1, ylim=c(0,15000), col='blue', 
        border=NA, add=TRUE)
barplot(A1$cik, names.arg=A1$filingyear, xaxs='i', space=1, ylim=c(0,15000), col='green', 
        border=NA, add=TRUE)
legend(x='bottom', ncol=2, legend=c("ciks", "unique ciks"), col=c("blue", "green"), pch=15)
abline(h=c(0, 15000), v=c(1,46))

###################################################################################################
## Top 100 filers
company.names <- X[, c("companyname", "cik")]
company.names <- unique(company.names)

o <- which(X$formtype %in% c('10-K', '10-K/A'))
A <- as.data.frame.matrix(table(X[o, c("cik", "filingyear")]))
A <- data.frame(cik = as.numeric(rownames(A)), n.ciks = rowSums(A))
A <- A[order(A$n.ciks, decreasing = TRUE),]
A <- A[1:10,]
A <- merge(A, company.names)
A <- A[order(A$n.ciks, decreasing = TRUE), ]

jpeg(filename = "top10-filers.jpeg", width=600, height=480, quality=100)
par(mar=c(5,24,4,2)+0.1)
barplot(A$n.ciks, horiz = TRUE, names.arg = toupper(A$companyname), col='blue', xlab='No. Filings', las=2, cex.names=.75)
dev.off()
write.table(A, "download-filings/top-filers.txt", sep="\t")
