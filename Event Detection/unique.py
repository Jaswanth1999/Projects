# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 18:52:14 2020

@author: jaswa
"""

import pandas as pd
import numpy as np
import csv
import os
import chardet


path = 'GenSyncs/'

#files = os.listdir(path)
d = pd.read_csv("LabelledSyncs_ICWSM.csv")
files = d.values[:,0]
files = files + ".csv"
with open('unique_users_ICWSM.csv', mode='w',encoding="utf8") as employee_file:
    for file in files:
        print(file)
        
        try:
            data = pd.read_csv(path+file)
        except:
            data = pd.read_csv(path+file,encoding='ISO-8859-1')
        users = list(data.loc[:,'user_id'])
        unique_users = np.unique(users)
        d = [file.split(".")[0]]
        d.extend(unique_users)
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')
        employee_writer.writerow(d)