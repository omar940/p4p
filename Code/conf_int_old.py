#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 13:01:52 2018

@author: omarmgad
"""
import numpy as np
import matplotlib.pyplot as plt

def conf_int_old(df, n):
    #calculates statistics (collaborative mean, confidence intervals) and plots the data bsed on confidence interval (old MARCQI method)
    
    #calculate the collaborative mean
    collab_mean = df['ECF_mean'].mean(axis=0)
    
    #confidence interval calculation: X_bar +/- z_score*sigma/sqrt(n)
    z_scores = {
        50 : 0.674,
        70 : 1.04,
        75 : 1.15,
        80 : 1.28,
        90 : 1.645,
        95 : 1.96,
        99 : 2.58,
        }
    conf_int = 80 #set confidence interval; looks up value in dictionary
    z_score = z_scores[conf_int] 
    #https://pandas.pydata.org/pandas-docs/version/0.21/generated/pandas.DataFrame.sort_values.html

    #begin ploting
    fig1, ax1 = plt.subplots(1,1,figsize=(10,20))
    ax1.set_title('Profiling of Sites based on ECF relative to Collaborative Mean')
    
    #plot error bars
    for i in range(n):
        x_bar=z_score*df.iloc[i,1]/np.sqrt(n)
        #if lower bound is greater than the mean than place in top category
        if df.iloc[i,0]-x_bar > collab_mean:
            better = ax1.errorbar(df.iloc[i,0], df.index[i], xerr=x_bar, color='lightgreen', fmt='o', label='Better than Collaborative')
        #if upper bound is less than the mean than place in lowest category    
        elif df.iloc[i,0]+x_bar < collab_mean:
            worse = ax1.errorbar(df.iloc[i,0], df.index[i], xerr=x_bar, color='red', fmt='o', label='Worse than Collaborative')
        #otherwise place in middle category
        else:
            middle = ax1.errorbar(df.iloc[i,0], df.index[i], xerr=x_bar, color='orange', fmt='o', label='Average')
        
    #https://matplotlib.org/gallery/statistics/errorbar_features.html
    ax1.set_xlabel('ECF (%) with {}% Confidence Interval'.format(round(conf_int)))
    ax1.set_ylabel('Rank')
    collab_line = ax1.axvline(x=collab_mean, label = "Collaborative Mean", linestyle='--', color="purple")
    
    #https://stackoverflow.com/questions/24988448/how-to-draw-vertical-lines-on-a-given-plot-in-matplotlib
    plt.legend(handles=[collab_line, better, middle, worse])
    for i in range(n):
        if i == n-1:
            ax1.annotate("Site #"+str(df.loc[i+1,'site #']), (df.iloc[i,0]+x_bar,df.index[i]), fontsize=6)
        else:
            ax1.annotate(df.loc[i+1,'site #'], (df.iloc[i,0]+x_bar,df.index[i]), fontsize=6)
                            
    plt.show()