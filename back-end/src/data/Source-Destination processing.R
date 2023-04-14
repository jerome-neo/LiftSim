# Computes the proportion of source-destination pairs from the raw data.
# The R list `proportions` contains tibble dataframes of proportions at off-peak,
# morning peak, afternoon peak, and evening peak periods respectively.
# Use str(proportions) for more info.
# Proportions are for use in generating Persons in simpy using Poisson process.

library(readxl)
library(dplyr)

dat <- list()
proportions <- list()

for (i in 1:4) {
  dat[[i]] <- read_excel("Source-Destination.xlsx", sheet=i)
  n <- sum(dat[[i]]$Count)
  
  proportions[[i]] <- dat[[i]] %>%
    group_by(Source, Dest) %>%
    summarize(p=sum(Count)/n)
  
  write.csv(proportions[[i]], paste("prop", i, ".csv", sep=""))
}

