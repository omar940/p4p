#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 07:11:36 2018

@author: omarmgad
"""
import pandas as pd
#imports dataframe with site rates, n for each site extracted from MARCQI_CoordCenter_Overview_Uni_Hip_30JUN2017.pdf (only with complete data)
#did not calculate APF
def abc_method(df, benchmark, n):
    #sort by site_rate
    abc_list = []
    
    #calculate APF
    df['APF'] = (df['Numerator']+1)/(df['total']+2)*100
    df_abc = df.sort_values(by='APF')
    
    #df_abc = df.sort_values(by='pred100')
    df_abc = df_abc.reset_index(drop=True)
    
    df_abc['CumSum'] = df_abc['total'].cumsum()
    df_abc['CumSum %'] = df_abc['CumSum']/df_abc['total'].sum()
    
    for k in range(len(benchmark)):
        
        #find total number of patients: n_total
        
        for i in range(n):
            if df_abc.loc[i, 'CumSum %'] > benchmark[k]:
                break
            #exit while loop when n_denom/n>10%
            else:
                continue
        benchmark_value = df_abc.loc[:i, 'APF'].mean()
        abc_list.append(benchmark_value)
    return(abc_list, df_abc)

df = pd.read_csv('MARCQI_Forest_Data_HIP_SNF_REHAB_20JUN2018_Omar.csv').dropna()
