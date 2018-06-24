#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 07:11:36 2018

@author: omarmgad
"""
#imports dataframe with site rates, n for each site extracted from MARCQI_CoordCenter_Overview_Uni_Hip_30JUN2017.pdf (only with complete data)
def abc_method(df, benchmark, n):
    #sort by site_rate
    abc_list = []
    for k in range(len(benchmark)):
        df_abc = df.sort_values(by='Site_Rate')
        df_abc = df_abc.reset_index(drop=True)
        #find total number of patients: n_total
        n_total = df_abc['Number'].sum()
        #number of patients in numerator: n_bench
        n_bench = 0
        
        for i in range(n):
            #as long as fraction of patients is less than <10% (benchmark) add next hospital to n_bench
            if n_bench/n_total <= benchmark[k]:
                n_bench = n_bench + df_abc.loc[i, 'Number']
            #exit while loop when n_bench/n>10%
            else:
                break
        site_weight = []
        n_weight = []
        for j in range(i):
            n_weight=(df_abc.loc[j, 'Number']/n_bench)
            #print(df_abc.loc[j, 'Number'])
            #print(n_weight)
            #print(df_abc.loc[j, 'Site_Rate'])
            site_weight.append(n_weight*df_abc.loc[j, 'Site_Rate'])
    #        print(df_abc.loc[j, 'Number']/n_bench*df_abc.loc[j, 'Site_Rate'])
        #list of sites in subset: site_subset        
        #weight each hospital based on n of each site: site_weight
        #find performance by sum of site_rate*n_weight for all hospital in subset (site_subset)
        benchmark_value = sum(site_weight)
        abc_list.append(benchmark_value)
    return(abc_list)