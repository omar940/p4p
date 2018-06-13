#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 17:02:04 2018

@author: omarmgad

Compares three techniques for calculating P4P points. First takes data (means for all sites, with lower and upper CI calculated) as CSV file and fits distribution to perform Monte Carlo Simulation with n=10000. Then assigns P4P points based on Confidence Interval System, Linear Point Estimate, and Piecewise Function. To calculate benchmarks for Piecewise Function, the fitted distribution is used to calculate the max, target, and threshold. Histograms of the assignment of P4P points are created to compare the distribution of P4P points. Outputs all figures into PDF file. 

Distributions were fitted to for range of confidence intervals which was used to perform a Monte Carlo Simulation (i.e. calculate upper, lower CI for each sample). Upper and lower bound were assummed to be symmetric.
"""

#import basic modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#curve fitting and mc sim
#from monte_carlo import monte_carlo
#from curve_fitting import dist_fit

#import P4P assignment modules
from point_sys import point_sys
from benchmarking import benchmarking
from conf_int_old import conf_int_old
from conf_int_mc import conf_int_mc
from histo import histo
from optimize_curve import load_data
from multipage import multipage

#%%Import file and calculate basic parameters, run curve fitting and montecarlo simulation
plt.close('all')
df = pd.read_csv('MARCQI_Hip_Forest_Rates_08JAN2018_P4P_ECF.csv').dropna()
site_rate_str = 'Site_Rate'
L95_str = 'Site_Rate_L95'
U95_str = 'Site_Rate_U95'
CI_str = 'Site_Rate_CI'
CI_data = df[U95_str]-df[L95_str]
#calculates samples from fitted distribtuion for means
samples_site_rate, benchmarks = load_data(df[site_rate_str], site_rate_str)
df_mc = pd.DataFrame(data=samples_site_rate, columns=[site_rate_str])

#calculate samples from fitted distribution for confidence intervals
samples_CI = load_data(CI_data, CI_str)
#samples_L95 = load_data(df[L95_str], L95_str)
#samples_U95 = load_data(df[U95_str], U95_str)
#df_mc[L95_str]=pd.Series(samples_L95[0])
#df_mc[U95_str]=pd.Series(samples_U95[0])
df_mc[L95_str]=pd.Series(samples_site_rate-samples_CI[0]/2)
df_mc[U95_str]=pd.Series(samples_site_rate+samples_CI[0]/2)
for i in range(len(df_mc[L95_str])):
    if df_mc.loc[i, L95_str]<0:
        df_mc.loc[i, L95_str]=0

n_mc = df_mc.count().iloc[0] # number of sites
n = df.count().iloc[0] # number of sites

#indexes by 1 to number of sites
df_mc = df_mc.set_index(pd.Series(np.arange(1,n_mc+1)))
df = df.set_index(pd.Series(np.arange(1,n+1)))
    
#%%Performs analyses to determinei P4P points

conf_int_old(df, n)
collab_mean_14 = df.loc[1,'Avg_2014']
conf_int_mc(df_mc, n_mc, collab_mean_14)

v1=[]
v2=[]
v1 = point_sys(df_mc, n_mc)
v2 = benchmarking(df_mc, n_mc, benchmarks)
v = [v1, v2]
histo(v)
multipage('figures/output.pdf')

