#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 13:01:52 2018

@author: omarmgad
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def benchmarking(df, n, benchmarks):
    #calculates point-based P4P points and plots results
    
    df['P4P_bench'] = pd.Series()
    df['Category'] = pd.Series()
    
    #%%calculate the collaborative mean for 2014 and 2018
    #collab_mean = df.loc[1,'Avg_2014']
    ECF_mean = df['Site_Rate'].mean(axis=0)
    ECF_max = df['Site_Rate'].max(axis=0)
    ECF_min = df['Site_Rate'].min(axis=0)
    ECF_std = df['Site_Rate'].std(axis=0)
    
    #http://www.pindling.org/Math/Learning/Statistics/z_scores_table.htm
#    ECF_maxpts = -1.036*ECF_std+ECF_mean #15th percentile
#    ECF_target = 0.524*ECF_std+ECF_mean #70th percentile
#    ECF_threshold = 2.326*ECF_std+ECF_mean #99th percentile
    ECF_maxpts = benchmarks[0]
    ECF_target = benchmarks[1]
    ECF_threshold = benchmarks[2]
    
    max_P4P = 7.5
    mid_P4P = 5
    #m = (y2-y1)/(x2-x1); (x1=ECF_min, y1=7.5), (x2=ECF_max, y2=0)
    m1 = (mid_P4P-max_P4P)/(ECF_target-ECF_maxpts)
    #b = y - mx
    b1 = max_P4P-m1*ECF_maxpts
    
    m2 = (0-mid_P4P)/(ECF_threshold-ECF_target)
    b2 = 0-m2*ECF_threshold

    #%%begin plotting
    fig6, ax6 = plt.subplots(1,1,figsize=(10,20))
    ax6.set_title('Point-Based P4P for Standardized Risk of Discharge to SNF or Inpatient Rehabilitation\nPrimary Total Hip Arthroplasty, Monte Carlo Simulation\nPiecewise Payout Curve')
    ax6.grid(color='b', linestyle='-', linewidth=.05)
       
    max_label = 'Maximum (<15%)'
    target_label = 'Met Target (<70%)'
    thresh_label = 'Met Threshold (<95%)'
    outlier_label = 'Outliers (>95%)'
    #assign P4P points
    for i in range(1,n+1):
        if df.loc[i,'Site_Rate']<=ECF_maxpts:
            df.loc[i,'P4P_bench']=max_P4P
            df.loc[i,'Category']=max_label
        elif df.loc[i,'Site_Rate']<=ECF_target and df.loc[i,'Site_Rate']>ECF_maxpts:
            df.loc[i,'P4P_bench']=round(df.loc[i,'Site_Rate']*m1+b1,2)
            df.loc[i,'Category']=target_label
        elif df.loc[i,'Site_Rate']<=ECF_threshold and df.loc[i,'Site_Rate']>ECF_target:
            df.loc[i,'P4P_bench']=round(df.loc[i,'Site_Rate']*m2+b2,2)
            df.loc[i,'Category']=thresh_label
        else:
            df.loc[i,'P4P_bench']=0
            df.loc[i,'Category']=outlier_label
     #create vectors for plotting payout curves
    #line zero for max P4P points
    x_0 = np.arange(ECF_min-1, ECF_maxpts, 0.1)
    y_0 = [max_P4P]*len(x_0)
    #line one for meeting target
    x_1 = np.arange(ECF_maxpts, ECF_target, 0.1)
    y_1 = m1*x_1+b1
    #line two for meeting target
    x_2 = np.arange(ECF_target, ECF_threshold, 0.1)
    y_2 = m2*x_2+b2
    #line three for zero points
    x_3 = np.arange(ECF_threshold, ECF_max+1, 0.1)
    y_3 = [0]*len(x_3)
    x = [x_0, x_1, x_2, x_3]
    y = [y_0, y_1, y_2, y_3]
    
    counts = pd.value_counts(df['Category'].values, ascending=True)
    labels = []
    for i in range(len(counts)):
        string = [counts.axes[0][i], str(counts.loc[counts.axes[0][i]]), 'Sites']
        labels.append(' '.join(string))
    labels.sort()   
        
#    labels = [max_label+str(counts.loc[max_label])+' Sites', target_label+str(counts.loc[target_label])+' Sites', thresh_label+str(counts.loc[thresh_label])+' Sites', outlier_label+str(counts.loc[outlier_label])+' Sites']
    
    colors = ['lightgreen', 'tan', 'blue', 'orange']
    for i in range(len(x)):
        ax6.plot(x[i], y[i], label=labels[i], color=colors[i], alpha=.5, linewidth=7.0, zorder=1)
        
    #ax6.scatter(df.loc[:,'Site_Rate'], df.loc[:,'P4P_bench'], label='Actual P4P Points', color='red', linewidths=0.5, edgecolors='black', zorder=2, s=10)
    y_mark = [max_P4P, y_1[-1], y_2[-1]]
    marker_labels = [max_label, target_label, thresh_label]
    ax6.scatter(benchmarks, y_mark, color='red', linewidths=0.5, marker='*',edgecolors='black', zorder=2, s=100)
    for k in range(len(benchmarks)):
        ax6.annotate(marker_labels[k], (benchmarks[k], y_mark[k]))
    
    plt.ylim([-0.1, max_P4P+0.3])
    plt.yticks(np.arange(0, max_P4P+0.5, 0.5))        
        
    #https://matplotlib.org/gallery/statistics/errorbar_features.html
    ax6.set_xlabel('ECF/Rehab (%)')
    ax6.set_ylabel('P4P Points')
    #plt.yticks(np.arange(1,n), df['Short_Name'], fontsize=6)
    #ax6.axvline(x=collab_mean, label = "Collaborative Mean for 2014", linestyle='--', color="purple")
    ax6.axvline(x=ECF_mean, label = "Collaborative Mean", linestyle='--', color="magenta")
    
    #https://stackoverflow.com/questions/24988448/how-to-draw-vertical-lines-on-a-given-plot-in-matplotlib
    ax6.legend(loc=0)
    
        
                            
    #%%plot histogram (distribution of providers)
    v = list(df.loc[:,'P4P_bench'])
    return(v)