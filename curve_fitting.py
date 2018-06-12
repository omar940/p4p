#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 16:30:11 2018

@author: omarmgad
"""

from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt

def dist_fit(df):
    # create some normal random noisy data
    ser = df['Site_Rate']
    
    # plot normed histogram
    plt.hist(ser, density=True, edgecolor='black')
    
    # find minimum and maximum of xticks, so we know
    # where we should compute theoretical distribution
    xt = plt.xticks()[0]  
    xmin, xmax = min(xt), max(xt)  
    lnspc = np.linspace(xmin, xmax, len(ser))
    
    
    # lets try the normal distribution first
    m, s = stats.norm.fit(ser) # get mean and standard deviation  
    pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
    plt.plot(lnspc, pdf_g, label="Norm") # plot it
    
    # exactly same as above
    ag,bg,cg = stats.gamma.fit(ser)  
    pdf_gamma = stats.gamma.pdf(lnspc, ag, bg,cg)  
    plt.plot(lnspc, pdf_gamma, label="Gamma")
    
    # guess what :) 
    ab,bb,cb,db = stats.beta.fit(ser)  
    pdf_beta = stats.beta.pdf(lnspc, ab, bb,cb, db)  
    plt.plot(lnspc, pdf_beta, label="Beta")
    
    plt.legend(loc=0)
    
    plt.show()  
    