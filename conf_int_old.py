#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 13:01:52 2018

@author: omarmgad
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def conf_int_old(df, n):
    #calculates statistics (collaborative mean, confidence intervals) and plots the data bsed on confidence interval (old MARCQI method). Also assigns P4P and makes histogram.
   
    df['P4P'] = pd.Series()
    
    #calculate the collaborative mean
    collab_mean = df.loc[1,'Avg_2014']
    ECF_mean = df['Site_Rate_ECF'].mean(axis=0)

    #begin ploting
    fig1, ax1 = plt.subplots(1,1,figsize=(10,20))
    ax1.set_title('95% CIs for Standardized Risk of Discharge to SNF or Inpatient Rehabilitation\nPrimary Total Hip Arthroplasty, 01OCT2016-30SEP2017')
    ax1.grid(color='b', linestyle='-', linewidth=.05)
    
    #plot error bars
    for i in range(1,n+1):
        lower_error = np.array([df.loc[i,'Site_Rate_ECF']-df.loc[i,'Site_Rate_L95']])
        upper_error = np.array([df.loc[i,'Site_Rate_U95']-df.loc[i,'Site_Rate_ECF']])
        asymm_error = [lower_error, upper_error]
        #if lower bound is greater than the mean than place in bottom category
        #if lower bound is greater than the mean than award 7.5 P4P points
        if df.loc[i,'Site_Rate_U95'] < collab_mean:
            better = ax1.errorbar(df.loc[i,'Site_Rate_ECF'], df.index[i-1], xerr=asymm_error, color='lightgreen', fmt='o', label='Better than Collaborative', elinewidth=3)
            df.loc[i,'P4P']=7.5
        
        #if upper bound is less than the mean than place in lowest category    
        #if upper bound is less than the mean than award 0 points 
        elif df.loc[i,'Site_Rate_L95'] > collab_mean:
            worse = ax1.errorbar(df.loc[i,'Site_Rate_ECF'], df.index[i-1], xerr=asymm_error, color='orange', fmt='o', label='Worse than Collaborative', elinewidth=3)
            df.loc[i,'P4P']=0
        #otherwise place in middle category with 5 points
        else:
            middle = ax1.errorbar(df.loc[i,'Site_Rate_ECF'], df.index[i-1], xerr=asymm_error, color='tan', fmt='o', label='Average', elinewidth=3)
            df.loc[i,'P4P']=5
            
        #ax1.annotate(df.loc[i,'Short_Name'], (3, df.index[i-1]), fontsize=6)
        
    #https://matplotlib.org/gallery/statistics/errorbar_features.html
    ax1.set_xlabel('ECF (days) with 95% Confidence Interval')
    ax1.set_ylabel('Hospital')
    plt.yticks(np.arange(1,n+1), df['Short_Name'], fontsize=6)
    collab_line = ax1.axvline(x=collab_mean, label = "Collaborative Mean for 2014", linestyle='--', color="purple")
    collab_line1 = ax1.axvline(x=ECF_mean, label = "Collaborative Mean for 2017", linestyle='--', color="magenta")
    
    #https://stackoverflow.com/questions/24988448/how-to-draw-vertical-lines-on-a-given-plot-in-matplotlib
    ax1.legend(handles=[collab_line, collab_line1, better, middle, worse], loc=0)
    
        
                            
    #plot histogram
    v = list(df.loc[:,'P4P'])
    x_pos = [0, 5, 7.5]
    labels = ['0', '5', '7.5']
    height = [v.count(0), v.count(5), v.count(7.5)]
    
    fig2, ax2 = plt.subplots(1,1,figsize=(10,20))
    
    #num_bins = 4
    #n, bins, patches = ax2.hist(v, num_bins, color='blue', alpha=0.5, edgecolor='black', linewidth=1.2)
    plt.bar(x_pos, height, edgecolor='black', width=2.5)
    plt.xticks(x_pos, labels)
    #plt.xticks(num_bins, labels)
    
    plt.xlabel('P4P Points')
    plt.ylabel('Number of Hospitals')
    plt.title(r'MARCQI Site Distribution of P4P Points')
    
    plt.show()