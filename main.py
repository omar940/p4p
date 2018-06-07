#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 17:02:04 2018

@author: omarmgad
"""

import pandas as pd
from monte_carlo import monte_carlo
from point_sys import point_sys
from conf_int_old import conf_int_old

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab


'''Calculates confidence intervals given 'n' sites and pandas dataframe which includes mean and standard deviation for each sample. Monte Carlo simulation can be changed by modifying 'x' to increase number of iterations (results in average of ECF_means across all simulations). Also plots the result as a forest plot.'''

df = pd.read_csv('MARCQI_Hip_Forest_Rates_08JAN2018_P4P.csv').dropna()
n = df.count().iloc[4] # number of sites
x_iter = 10 # number of iterations for Monte Carlo simulation
ECF_mean = df['Site_Rate_ECF'].mean(axis=0)
ECF_std = df['Site_Rate_ECF'].std(axis=0)

x = np.linspace(ECF_mean - 3*ECF_std, ECF_mean + 3*ECF_std, 100)
plt.plot(x,mlab.normpdf(x, ECF_mean, ECF_std))
plt.hist(df['Site_Rate_ECF'], density=True, bins=25, alpha=0.5, color='g', edgecolor='black', linewidth=1.2)
#plt.grid(True)
plt.xlabel('ECF (days)')
plt.ylabel('Probability')
plt.title('Histogram of ECF for MARCQI')
plt.show()

#df = monte_carlo(df, x)

df_rank = df.rank()
df = df.set_index(df_rank.iloc[:,0])
#indexes by rank intead of site number, there's still a column for site number for record keeping

#point_sys(df, n)
conf_int_old(df, n)
