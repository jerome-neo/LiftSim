library(coda)
library(readxl)

# initialize data
traffic <- read_excel("Traffic Counts.xlsx")

mrn_counts <- traffic$count[1:9]
aft_counts <- traffic$count[10:18]
off_counts <- traffic$count[19:27]
evn_counts <- traffic$count[28:36]

# initialize function to perform gibbs sampling
gibbs <- function(y){
  lambda <- 0.007; phi <- 0.007; theta <- 0.007
  m <- 1; n <- 4
  
  for (t in 1:12000){
    lambda[t+1] <- rgamma(1, sum(y[1:m[t]])+1, m[t])
    phi[t+1] <- rgamma(1, sum(y[(m[t]+1):n[t]])+1, n[t]-m[t])
    theta[t+1] <- rgamma(1, sum(y[(n[t]+1):9])+1, 9-n[t])
    
    log_ratio <- function(i){
      return((sum(y[1:i]))*log(lambda[t+1])+(sum(y[(i+1):n[t]]))*log(phi[t+1])-i*lambda[t+1]-(n[t]-i)*phi[t+1])
    }
    
    max_log_ratio <- 0
    for (i in 1:(n[t]-1)){
      if (max_log_ratio < log_ratio(i)){
        max_log_ratio <- log_ratio(i)
      }
    }
    
    while (length(m) < t+1){
      V <- sample(1:(n[t]-1), 1)
      if (log(runif(1)) <= log_ratio(V) - max_log_ratio){
        m[t+1] <- V
      }
    }
    
    log_ratio <- function(i){
      return((sum(y[(m[t+1]+1):i]))*log(phi[t+1])+(sum(y[(i+1):9]))*log(theta[t+1])-(i-m[t+1])*phi[t+1]-(9-i)*theta[t+1])
    }
    
    max_log_ratio <- 0
    for (i in (m[t+1]+1):8){
      if (max_log_ratio < log_ratio(i)){
        max_log_ratio <- log_ratio(i)
      }
    }
    
    while (length(n) < t+1){
      V <- sample((m[t+1]+1):8, 1)
      if (log(runif(1)) <= log_ratio(V) - max_log_ratio){
        n[t+1] <- V
      }
    }
  }
  return(list('lambda'=lambda, 'phi'=phi, 'theta'=theta, 'm'=m, 'n'=n))
}

# resulting posterior curve for morning counts
results_list <- gibbs(mrn_counts)

mcmc_lambda <- mcmc(results_list$lambda[2001:12000])
plot(mcmc_lambda)

mcmc_phi <- mcmc(results_list$phi[2001:12000])
plot(mcmc_phi)

mcmc_theta <- mcmc(results_list$theta[2001:12000])
plot(mcmc_theta)

mcmc_m <- mcmc(results_list$m[2001:12000])
plot(mcmc_m)

mcmc_n <- mcmc(results_list$n[2001:12000])
plot(mcmc_n)

# resulting posterior curve for afternoon counts
results_list <- gibbs(mft_counts)

mcmc_lambda <- mcmc(results_list$lambda[2001:12000])
plot(mcmc_lambda)

mcmc_phi <- mcmc(results_list$phi[2001:12000])
plot(mcmc_phi)

mcmc_theta <- mcmc(results_list$theta[2001:12000])
plot(mcmc_theta)

mcmc_m <- mcmc(results_list$m[2001:12000])
plot(mcmc_m)

mcmc_n <- mcmc(results_list$n[2001:12000])
plot(mcmc_n)

# resulting posterior curve for off-peak counts
results_list <- gibbs(off_counts)

mcmc_lambda <- mcmc(results_list$lambda[2001:12000])
plot(mcmc_lambda)

mcmc_phi <- mcmc(results_list$phi[2001:12000])
plot(mcmc_phi)

mcmc_theta <- mcmc(results_list$theta[2001:12000])
plot(mcmc_theta)

mcmc_m <- mcmc(results_list$m[2001:12000])
plot(mcmc_m)

mcmc_n <- mcmc(results_list$n[2001:12000])
plot(mcmc_n)

# resulting posterior curve for evening counts
results_list <- gibbs(evn_counts)

mcmc_lambda <- mcmc(results_list$lambda[2001:12000])
plot(mcmc_lambda)

mcmc_phi <- mcmc(results_list$phi[2001:12000])
plot(mcmc_phi)

mcmc_theta <- mcmc(results_list$theta[2001:12000])
plot(mcmc_theta)

mcmc_m <- mcmc(results_list$m[2001:12000])
plot(mcmc_m)

mcmc_n <- mcmc(results_list$n[2001:12000])
plot(mcmc_n)