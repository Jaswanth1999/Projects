# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 11:52:40 2020

@author: jaswa
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


D1 = pd.read_csv("climbing_stairs.csv")
d2 = pd.read_csv("walking1.csv")
d3 = pd.read_csv("jogging.csv")
d4 = pd.read_csv("jumping.csv")

d1 = []
for i in D1.values[:,0]:
    d1.append(int(i.split()[2]))
    
d2 = d2.values[:,1]
d3 = d3.values[:,1]
d4 = d4.values[:,1]


slice = 20

D = []

for i in range(0,len(d1)-slice):
    x = d1[i:i+slice]
    x.append(0)
    D.append(x)
    
for i in range(0,len(d2)-slice):
    x = list(d2[i:i+slice])
    x.append(1)
    D.append(x)

for i in range(0,len(d3)-slice):
    x = list(d3[i:i+slice])
    x.append(2)
    D.append(x)

for i in range(0,len(d4)-slice):
    x = list(d4[i:i+slice])
    x.append(3)
    D.append(x)
    
    
Data = pd.DataFrame(D)

Data.to_csv("Data.csv")

font = 20

plt.figure(figsize=(16,8))
#plt.title("Climbing Stairs")
plt.xlabel("Time (ms) ")
ini = 155
plt.plot(range(len(d1[155:220])),d1[155:220])
for i in range(len(d1[155:220])):
    plt.plot(i,d1[ini+i],'-gD')
for i in range(20,29):
    plt.annotate(str(i-19),xy=(i,d1[ini+i]+11),fontsize=font)
plt.yticks(np.arange(0, 1024, 100)) 
plt.savefig("climbing_stairs.png")
plt.show()

plt.figure(figsize=(16,8))
#plt.title("Walking")
plt.xlabel("Time (ms) ")
plt.plot(range(len(d2[1300:1360])),d2[1300:1360])
ini = 1300
for i in range(len(d2[1300:1360])):
    plt.plot(i,d2[ini+i],'-gD')
for i in range(16,26):
    plt.annotate(str(i-15),xy=(i,d2[ini+i]+11),fontsize=font)
plt.yticks(np.arange(0, 1024, 100)) 
plt.savefig("walking.png")
plt.show()


plt.figure(figsize=(16,8))
#plt.title("Jogging")
plt.xlabel("Time (ms) ")
plt.plot(range(len(d3[470:530])),d3[470:530])
ini = 470
for i in range(len(d3[470:530])):
    plt.plot(i,d3[ini+i],'-gD')
for i in range(19,26):
    plt.annotate(str(i-18),xy=(i,d3[ini+i]+11),fontsize=font)
plt.yticks(np.arange(0, 1024, 100)) 
plt.savefig("jogging.png")
plt.show()


plt.figure(figsize=(16,8))
#plt.title("Jumping")
plt.xlabel("Time (ms) ")
plt.plot(range(len(d4[205:265])),d4[205:265])
ini = 205
for i in range(len(d3[205:265])):
    plt.plot(i,d4[ini+i],'-gD')
for i in range(19,26):
    plt.annotate(str(i-18),xy=(i,d4[ini+i]+11),fontsize=font)
plt.yticks(np.arange(0, 1024, 100)) 
plt.savefig("jumping.png")
plt.show()




