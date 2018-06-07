#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 13:01:52 2018

@author: omarmgad
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def point_sys(df, n):
    #calculates point-based P4P points and plots results
    
    df['P4P_point'] = pd.Series()
    
    #calculate the collaborative mean
    collab_mean = df.loc[1,'Avg_2014']
    ECF_mean = df['Site_Rate_ECF'].mean(axis=0)
    ECF_max = df['Site_Rate_ECF'].max(axis=0)
    ECF_min = df['Site_Rate_ECF'].min(axis=0)
    max_P4P = 7.5
    #m = (y2-y1)/(x2-x1); (x1=ECF_min, y1=7.5), (x2=ECF_max, y2=0)
    m = -max_P4P/(ECF_max-ECF_min)
    b = max_P4P-m*ECF_min

    #begin ploting
    fig3, ax3 = plt.subplots(1,1,figsize=(10,20))
    ax3.set_title('Point-Based P4P for Standardized Risk of Discharge to SNF or Inpatient Rehabilitation\nPrimary Total Hip Arthroplasty, 01OCT2016-30SEP2017')
    ax3.grid(color='b', linestyle='-', linewidth=.05)
    
    #plot error bars
    df.loc[:,'P4P_point']=round(df.loc[:,'Site_Rate_ECF']*m+b,2)
    ax3.plot(df.loc[:,'Site_Rate_ECF'], df.loc[:,'P4P_point'], label='Payout Curve', color='lightgreen')
    for i in range(1,n):
        if df.loc[i,'P4P_point']<0:
            df.loc[i,'P4P_point']=0
    
    #df_1 = df[(df != 0).all(1)]
    
    ax3.plot(df.loc[:,'Site_Rate_ECF'], df.loc[:,'P4P_point'], '+', label='Actual P4P Points', color='red')
    plt.ylim([-0.1, max_P4P+0.1])
    plt.yticks(np.arange(0, max_P4P+0.5, 0.5))        
            
        #ax3.annotate(df.loc[i,'Short_Name'], (3, df.index[i-1]), fontsize=6)
        
    #https://matplotlib.org/gallery/statistics/errorbar_features.html
    ax3.set_xlabel('ECF (days)')
    ax3.set_ylabel('P4P Points')
    #plt.yticks(np.arange(1,n), df['Short_Name'], fontsize=6)
    ax3.axvline(x=collab_mean, label = "Collaborative Mean for 2014", linestyle='--', color="purple")
    ax3.axvline(x=ECF_mean, label = "Collaborative Mean for 2017", linestyle='--', color="magenta")
    
    #https://stackoverflow.com/questions/24988448/how-to-draw-vertical-lines-on-a-given-plot-in-matplotlib
    ax3.legend(loc=0)
    
        
                            
    #plot histogram
    v = list(df.loc[:,'P4P_point'])
    #x_pos = [0, 1, 2]
    #labels = ['0', '5', '7.5']
    #height = [v.count(0), v.count(5), v.count(7.5)]
    
    fig4, ax4 = plt.subplots(1,1,figsize=(10,20))
    
    num_bins = 15
    n, bins, patches = ax4.hist(v, num_bins, facecolor='blue', alpha=0.5, edgecolor='black', linewidth=1.2)
    #plt.bar(x_pos, height, width=0.9)
    plt.xticks(np.arange(0, max_P4P+0.5, 0.5)) 
    #plt.xticks(num_bins, labels)
    
    plt.xlabel('P4P Points')
    plt.ylabel('Number of Hospitals')
    plt.title(r'MARCQI Site Distribution of P4P Points')
    
    plt.show()