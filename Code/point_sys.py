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
    
    #%%calculate the collaborative mean for 2014 and 2018
    #collab_mean = df.loc[1,'Avg_2014']
    ECF_mean = df['pred100'].mean(axis=0)
    ECF_max = df['pred100'].max(axis=0)
    ECF_min = df['pred100'].min(axis=0)
    max_P4P = 7.5
    #m = (y2-y1)/(x2-x1); (x1=ECF_min, y1=7.5), (x2=ECF_max, y2=0)
    m = -max_P4P/(ECF_max-ECF_min)
    b = max_P4P-m*ECF_min

    #%%begin plotting
    fig3, ax3 = plt.subplots(1,1,figsize=(10,20))
    ax3.set_title('Point-Based P4P for Standardized Risk of Discharge to SNF or Inpatient Rehabilitation\nPrimary Total Hip Arthroplasty, Monte Carlo Simulation\nLinear Payout Curve')
    #ax3.grid(color='b', linestyle='-', linewidth=.05)
    
    #plot error bars
    df.loc[:,'P4P_point']=round(df.loc[:,'pred100']*m+b,2)
    ax3.plot(df.loc[:,'pred100'], df.loc[:,'P4P_point'], label='Linear Payout Curve', color='lightgreen', alpha=.5, linewidth=7.0, zorder=1)
    for i in range(1,n+1):
        if df.loc[i,'P4P_point']<0:
            df.loc[i,'P4P_point']=0
        if df.loc[i,'P4P_point']>7.5:
            df.loc[i,'P4P_point']=7.5
    
    #df_1 = df[(df != 0).all(1)]
    
    #ax3.scatter(df.loc[:,'pred100'], df.loc[:,'P4P_point'], label='Actual P4P Points', c='red', linewidths=1.0, edgecolors='black', zorder=2)
    plt.ylim([-0.1, max_P4P+0.1])
    plt.yticks(np.arange(0, max_P4P+0.5, 0.5))        
            
        #ax3.annotate(df.loc[i,'Short_Name'], (3, df.index[i-1]), fontsize=6)
        
    #https://matplotlib.org/gallery/statistics/errorbar_features.html
    ax3.set_xlabel('ECF/Rehab (%)')
    ax3.set_ylabel('P4P Points')
    ax3.axvline(x=ECF_mean, label = "Collaborative Mean", linestyle='--', color="magenta")
    ax3.scatter([ECF_max, ECF_min], [0, max_P4P], color='red', linewidths=0.5, marker='*',edgecolors='black', zorder=2, s=300)
    
    #https://stackoverflow.com/questions/24988448/how-to-draw-vertical-lines-on-a-given-plot-in-matplotlib
    ax3.legend(loc=0)
    
        
                            
    #%%plot histogram (distribution of providers)
    v = list(df.loc[:,'P4P_point'])
    return(v)