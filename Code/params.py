#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 16:00:01 2018

@author: omarmgad
"""

import numpy as np
import pandas as pd


def params(n):
    '''Sets up parameters (mean and standard deviation) for 'n' sites and stores in pandas dataframe (df)'''

    #(b - a) * random_sample() + a; Unif[a, b), b > a 
    b1 = 40 #max ECF
    a1 = 8 #min ECF
    b2 = 14 #max STD for ECF
    a2 = 3 #min STD for ECF
    df = pd.DataFrame() 
    df.loc[:,'ECF_mean'] = pd.Series((b1-a1)*np.random.random_sample(n)+a1)
    df.loc[:,'ECF_sigma'] = pd.Series((b2-a2)*np.random.random_sample(n)+a2)
    df.loc[:,'site #'] = df.index
    #df2 = pd.DataFrame((b-a)*np.random.randn(1,n), index=['ECF_sigma'], columns=site_names)+a
    #Return a sample (or samples) from the “standard normal” distribution.
    
    return df

