# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 12:36:51 2020

@author: jaswa
"""

import os
import numpy as np
import pandas as pd


path ='D:\Proj\BTP\Friends_ICWSM'
path1 = 'D:\Proj\BTP'

dir_names = os.listdir("D:\Proj\BTP\Friends_ICWSM")


# for r, dirs, files in os.walk(path):
#     for d in files:
#         dir_names.append(d)
        

def average_common_friends(data):
    d = data[1:,1:]
    l,b = d.shape
    s = 0
    for i in range(0,l):
        for j in range(i+1,b):
            s = s+d[i,j]
            
    if l==1:
        return s
    count = (l*l-l)/2
    if count == 0:
        print(d)
        return 0
    avg = s/count
    return avg

os.chdir(path)
Avg_common_friends = []
for r, dirs, files in os.walk(path):
    for d in files:
        data = pd.read_csv(d)
        length = data.shape[0]-1
        avg = average_common_friends(data.values[:,:])
        name = d.split('.')[0]
        Avg_common_friends.append([name,length,avg])
        
df = pd.DataFrame(Avg_common_friends)
df.to_csv(path1 + '/Avg_common_friends_ICWSM.csv')
        
        