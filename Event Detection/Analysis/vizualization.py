# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:36:25 2020

@author: jaswa
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = "Non_Events/"
path2 = "Non_Events_plots/"


files = os.listdir(path)

for file in files:
    d = pd.read_csv(path+file)
    data = d.values[1:,2:]
    
    degree = []
    
    for row in data:
        degree.append(sum(row)/len(row))
    
    
    m = int(max(degree))
    bin_size=10
    bin_list= list(range(0,m+bin_size,bin_size))
    plt.figure(figsize=(40,8))
    plt.hist(degree,bins=bin_list,edgecolor='black', linewidth=1.2)
    plt.xticks(bin_list,rotation=90)
    plt.xlabel("Degree")
    plt.ylabel("No. of people")
    plt.title("Degree Distribution for"+file)
    plt.savefig(path2+file+"norm.jpg")
    plt.show()