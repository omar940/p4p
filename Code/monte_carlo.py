#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 12:16:58 2018

@author: omarmgad
"""
from params import params
import pandas as pd

def monte_carlo(n, x):
    #Monte Carlo simulation that performs 'x' iterations of calculating the mean and standard deviation for "n" sites. Outputs dataframe with average means across all sites (sorted from lowest to highest for graphing purposes), average standard deviations across all sites, and site #.
    df_means = pd.DataFrame()
    df_stds = pd.DataFrame()
    
    for i in range(x):
        if i == 0:
            df = params(n) #create "true" values for Monte Carlo (sampling from truth)
            df = df.sort_values(by=['ECF_mean'])
            df_means.loc[:,i] = pd.Series(df.iloc[:,0])
            #add ECF means to dataframe
            df_stds.loc[:,i] = pd.Series(df.iloc[:,1])
            #add ECF std to dataframe
        else:
            df = params(n) #create "true" values for Monte Carlo (sampling from truth)
            df = df.sort_values(by=['ECF_mean'])
            #converted to lists that we lose the index, allows us to assign the lowest values to site one
            dfList_means = df['ECF_mean'].tolist()
            dfList_stds = df['ECF_sigma'].tolist()
            df_means.loc[:,i] = dfList_means
            #add ECF means to dataframe
            df_stds.loc[:,i] = dfList_stds
            #add ECF std to dataframe
        
    #converts site number to rank so that forest plot looks cool
    
    df_final = pd.DataFrame()    
    df_final['ECF_mean'] = df_means.mean(axis=1)
    df_final['ECF_sigma'] = df_stds.mean(axis=1)
    df_final['site #'] = df.index
    
    return df_final