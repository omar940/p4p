#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 14:46:59 2018

@author: omarmgad
"""

from sas7bdat import SAS7BDAT
f = SAS7BDAT('midb_marcqi_common_all_14MAR2018.sas7bdat')
    
df = f.to_data_frame()