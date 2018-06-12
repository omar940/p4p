#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 17:02:04 2018

@author: omarmgad

Calculates confidence intervals given 'n' sites and pandas dataframe which includes mean and standard deviation for each sample. Monte Carlo simulation can be changed by modifying 'x' to increase number of iterations (results in average of ECF_means across all simulations). Also plots the result as a forest plot.
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
from optimize_curve import load_data, benchmarks_calc

#%%Import file and calculate basic parameters, run curve fitting and montecarlo simulation
plt.close('all')
df = pd.read_csv('MARCQI_Hip_Forest_Rates_08JAN2018_P4P_ECF.csv').dropna()
x_iter = 1000 # number of iterations for Monte Carlo simulation
site_rate_str = 'Site_Rate'
L95_str = 'Site_Rate_L95'
U95_str = 'Site_Rate_U95'

#calculates samples from fitted distribtuion for means
samples_site_rate, benchmarks = load_data(df[site_rate_str], site_rate_str)
df_mc = pd.DataFrame(data=samples_site_rate, columns=[site_rate_str])
#calculate samples from fitted distribution for confidence intervals
#samples_L95 = load_data(df[L95_str], L95_str)
#samples_U95 = load_data(df[U95_str], U95_str)
#df_mc[L95_str]=pd.Series(samples_L95)
#df_mc[U95_str]=pd.Series(samples_U95)

n_mc = df_mc.count().iloc[0] # number of sites
n = df.count().iloc[0] # number of sites

#indexes by 1 to number of sites
df_mc = df_mc.set_index(pd.Series(np.arange(1,n_mc+1)))
df = df.set_index(pd.Series(np.arange(1,n+1)))
    
#%%Performs analyses to determinei P4P points
v1=[]
v2=[]
#conf_int_old(df, n)
#conf_int_mc(df_mc, n_mc)
#v1 = point_sys(df_mc, n_mc)
v2 = benchmarking(df_mc, n_mc, benchmarks)
v = [v1, v2]
histo(v)
