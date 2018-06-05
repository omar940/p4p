#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 17:02:04 2018

@author: omarmgad
"""

from monte_carlo import monte_carlo
from ranking_plot import ranking_plot
from conf_int_old import conf_int_old

'''Calculates confidence intervals given 'n' sites and pandas dataframe which includes mean and standard deviation for each sample. Monte Carlo simulation can be changed by modifying 'x' to increase number of iterations (results in average of ECF_means across all simulations). Also plots the result as a forest plot.'''

n = 50 # number of sites
x = 100 # number of iterations for Monte Carlo simulation

df = monte_carlo(n, x)

df_rank = df.rank()
df = df.set_index(df_rank.iloc[:,0])
#indexes by rank intead of site number, there's still a column for site number for record keeping

ranking_plot(df, n)
conf_int_old(df, n)
