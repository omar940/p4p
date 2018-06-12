#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 12:16:58 2018

@author: omarmgad
"""
from params import params
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def monte_carlo(dist_samples, column_str):
    #Monte Carlo simulation that performs 'x' iterations of calculating the mean and standard deviation for "n" sites. Outputs dataframe with average means across all sites (sorted from lowest to highest for graphing purposes), average standard deviations across all sites, and site #.    
    df_mc = pd.DataFrame(data=dist_samples, columns=[column_str])
    #df_mc = pd.DataFrame(data=samples_L95, columns=['Site_Rate_L95'])
    #df_mc = pd.DataFrame(data=samples_U95, columns=['Site_Rate_U95'])
    #df_mc['Site_Rate_L95']=pd.Series(samples_L95)
    #df_mc['Site_Rate_U95']=pd.Series(samples_U95)
    
    #%%create distribution of data with histogram
    x = dist_samples
    plt.plot(x,mlab.normpdf(x, ECF_mean, ECF_std))
    plt.hist(df[column_str], density=True, bins=25, alpha=0.8, color='g', edgecolor='black', linewidth=1.2, label='Based on 2017 ECF Data')
    plt.hist(df_mc[column_str], density=True, bins=25, alpha=0.3, color='b', edgecolor='black', linewidth=1.2, label='Monte Carlo Simulation (n=1000)')
    #plt.grid(True)
    plt.xlabel('ECF/Rehab (%)')
    plt.ylabel('Probability')
    plt.title('Histogram of ECF for MARCQI')
    plt.legend(loc=0)
    plt.show()
    
    return df_mc