#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:24:17 2018

@author: omarmgad
"""

import numpy as np
import matplotlib.pyplot as plt

def histo(v):
    """Generates histograms for point estimate and benchmarking method"""
   
    #%%plot histogram (distribution of providers)
    max_P4P = 7.5
    fig4, ax4 = plt.subplots(1,1,figsize=(10,20))

    num_bins = int(max_P4P/0.5)
    ax4.hist(v[0], num_bins, facecolor='green', alpha=0.2, edgecolor='black', linewidth=1.2, label='Linear Incentive Curve', range=[0,max_P4P+1])
    ax4.hist(v[1], num_bins, facecolor='orange', alpha=0.5, edgecolor='black', linewidth=1.2, label='Piecewise Incentive Curve', range=[0,max_P4P+1])
    #plt.bar(x_pos, height, width=0.9)
    plt.xticks(np.arange(0, max_P4P+1, 0.5)) 
    #plt.xticks(num_bins, labels)
    
    plt.xlabel('P4P Points')
    plt.ylabel('Number of Hospitals')
    plt.title(r'MARCQI Site Distribution of P4P Points based on Monte Carlo Simulation')
    plt.legend(loc=0)
    
    plt.show()