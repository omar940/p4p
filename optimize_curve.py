#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 19:35:36 2018

@author: omarmgad
https://stackoverflow.com/questions/6620471/fitting-empirical-distribution-to-theoretical-ones-with-scipy-python
go here^ for a full list of distributions

returns the distribution with the least SSE (summed squared error) between the distribution's histogram and the data's histogram.
"""

import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

#%% Create models from data
def best_fit_distribution(data, bins=20, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    DISTRIBUTIONS = [        
        st.alpha,st.betaprime,st.bradford,st.burr,st.chi,st.chi2,
        st.expon,st.exponweib,st.exponpow,st.f,st.fisk,
        st.foldnorm,st.genlogistic,st.genexpon,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gompertz,
        st.halflogistic,st.halfnorm,st.halfgennorm,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.ksone,st.kstwobign,
        st.logistic,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.powerlaw,st.powerlognorm,
        st.rayleigh,st.rice,st.recipinvgauss,st.truncexpon,st.truncnorm,
        st.uniform,st.wald,st.weibull_min,st.wrapcauchy
    ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)

def make_pdf(dist, params, size=100):
    """Generate distributions's Propbability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf

# %%Load data from statsmodels datasets
def load_data(data, col_str):
    
    # Plot for comparison
    plt.figure(figsize=(12,8))
    ax = data.plot(kind='hist', bins=20, density=True, alpha=0.5) #color=plt.rcParams['axes.color_cycle'][1]
    # Save plot limits
    dataYLim = ax.get_ylim()
    
    # Find best fit distribution
    best_fit_name, best_fir_paramms = best_fit_distribution(data, 200, ax)
    best_dist = getattr(st, best_fit_name)
    
    # Update plots
    ax.set_ylim(dataYLim)
    ax.set_title(u'Standardized Risk of Discharge to SNF or Inpatient Rehabilitation\nPrimary Total Hip Arthroplasty\n All Fitted Distributions')
    ax.set_xlabel(u'ECF/Rehab (%)')
    ax.set_ylabel('Frequency')
    
    # Make PDF
    pdf = make_pdf(best_dist, best_fir_paramms)
    
    # Display
    plt.figure(figsize=(12,8))
    ax = pdf.plot(lw=2, label='PDF', legend=True)
    data.plot(kind='hist', bins=20, density=True, alpha=0.5, label='Data', legend=True, ax=ax)
    
    param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
    param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fir_paramms)])
    dist_str = '{}({})'.format(best_fit_name, param_str)
    
    ax.set_title(u'Standardized Risk of Discharge to SNF or Inpatient Rehabilitation\nPrimary Total Hip Arthroplasty with best fit distribution for ' + col_str + '\n' + dist_str)
    ax.set_xlabel(u'ECF/Rehab (% of patients)')
    ax.set_ylabel('Frequency')
    
    dist_samples = gen_rand(best_dist, best_fir_paramms)
    benchmarks = benchmarks_calc(best_dist, best_fir_paramms)
    return dist_samples, benchmarks
    
#%% generate random numbers    
def gen_rand(dist, params, size=1000):
    """Generate distribution's random numbers"""
    
    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    
    # generate random numbers
    dist_samples = dist.rvs(*arg, loc=loc, scale=scale, size=size)
    return dist_samples

def benchmarks_calc(dist, params):
    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    
    #generate benchmarks
    maxpts = dist.ppf(0.15, *arg, loc=loc, scale=scale)
    target = dist.ppf(0.70, *arg, loc=loc, scale=scale)
    threshold = dist.ppf(0.95, *arg, loc=loc, scale=scale)
    benchmarks = [maxpts, target, threshold]

    return benchmarks
    
