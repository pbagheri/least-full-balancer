# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:01:31 2019

@author: payam.bagheri
"""

# this code was written to simulate a balancer to help calculating brand usage incidences

import pandas as pd
import numpy as np
from os import path
from tqdm import tqdm
#from cx_Freeze import setup, Executable

dir_path = path.dirname(path.dirname(path.abspath(__file__)))
print(dir_path)

data = pd.read_csv(dir_path + '/0_input_data/2006-brand-usage-data.csv')
data.head()

data_PM = data.replace({0:1, 1:0, 2:0, 3:0, 4:0}) # defines PM qulaifiers
data_P3M = data.replace({0:1, 1:1, 2:0, 3:0, 4:0}) # defines P3M qulaifiers

quotas_PM = [300, 250, 300, 200] # different quotas for diff cells
quotas_P3M = [300, 200, 200, 250]
cells_PM = pd.DataFrame(columns=data.columns, index = [0]) # collects PM users
cells_PM.fillna(1, inplace = True)

cells_P3M = pd.DataFrame(columns=data.columns, index = [0]) # collects P3M users
cells_P3M.fillna(1, inplace = True) 

cells_PM_temp = cells_PM.copy()
cells_P3M_temp = cells_P3M.copy()

counter_PM = 0
counter_P3M = 0
first_time_PM = np.ones(len(quotas_PM))
first_time_P3M = np.ones(len(quotas_PM))

for i in tqdm(data.index): # loops through all responses
    if list(cells_PM.loc[0]) != quotas_PM:        
        counter_PM += 1
        if data_PM.loc[i].sum() != 0: # checks to make sure the resp could potentially qualify
            mul = np.multiply(list(data_PM.loc[i]),cells_PM_temp) # finds potential cells for the resp
            mul = mul.replace(0,np.nan) # replaces 0 with nan, so that 0 does not show up as least full. 0 was the result of not qualifying
            if mul.any().sum() != 0: # checks to make sure the resp qulifes for the non-filled cells
                mincol = mul.idxmin(axis=1) # find the col-name of the least full
                if cells_PM_temp[mincol].loc[0].item() < quotas_PM[int(mincol)]:
                    if first_time_PM[int(mincol[0])] == 1:
                        first_time_PM[int(mincol[0])] = 2
                    else:
                        cells_PM[mincol] += 1 # increases the count of the least full cell
                        cells_PM_temp[mincol] += 1
                        if cells_PM_temp[mincol].loc[0].item() == quotas_PM[int(mincol)]: # checks if the quota is reached
                            cells_PM_temp[mincol] = np.nan # removes the filled cells from race
            #print(cells_PM)
            
    if list(cells_P3M.loc[0]) != quotas_P3M:        
        counter_P3M += 1
        if data_P3M.loc[i].sum() != 0: # checks to make sure the resp could potentially qualify
            mul = np.multiply(list(data_P3M.loc[i]),cells_P3M_temp) # finds potential cells for the resp
            mul = mul.replace(0,np.nan) # replaces 0 with nan, so that 0 does not show up as least full. 0 was the result of not qualifying
            if mul.any().sum() != 0: # checks to make sure the resp qulifes for the non-filled cells
                mincol = mul.idxmin(axis=1) # find the col-name of the least full
                if cells_P3M_temp[mincol].loc[0].item() < quotas_P3M[int(mincol)]:
                    if first_time_P3M[int(mincol[0])] == 1:
                        first_time_P3M[int(mincol[0])] = 2
                    else:
                        cells_P3M[mincol] += 1 # increases the count of the least full cell
                        cells_P3M_temp[mincol] += 1
                        if cells_P3M_temp[mincol].loc[0].item() == quotas_P3M[int(mincol)]: # checks if the quota is reached
                            cells_P3M_temp[mincol] = np.nan # removes the filled cells from race
            #print(cells_P3M)
            
    if (list(cells_PM.loc[0]) == quotas_PM and list(cells_P3M.loc[0]) == quotas_P3M):
        break

print('number of resps needed', counter_PM, '\n')
print(list(cells_PM.loc[0]))


print('number of resps needed', counter_P3M, '\n')
print(list(cells_P3M.loc[0]))
    

