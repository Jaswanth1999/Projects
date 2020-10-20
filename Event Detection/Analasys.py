# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 18:42:44 2020

@author: jaswa
"""

import pandas as pd
import numpy as np
import random as rn





ann = pd.read_csv("LabelledSyncs_ICWSM.csv")
avg_frds = pd.read_csv("Avg_common_friends_ICWSM.csv")



# st = []

# for i in avg_frds.values[:,:]:
    
#     j,k = i[1].split('_')
#     j = j[4:]
#     k = k.split('.')[0]
#     st.append([k+j,i[3]])

st = avg_frds.values[:,[1,3]]

annotations = {}
avg={}
event=[]
non_event = []

for i in ann.values[:,:]:
    annotations[i[0]] = i[1]
    if i[1] == "EVENT":
        event.append(i[0])
    else:
        non_event.append(i[0])

for i in st:
    avg[i[0]] = i[1]


    
import random

r1 = random.sample(range(len(event)),int(len(event)/2))

r2 = random.sample(range(len(non_event)),int(len(non_event)/2))
  
    
l1 = []
l2 = []

for i in r1:
    l1.append(avg[event[i]])
    
for i in r2:
    l2.append(avg[non_event[i]])
    

m1 = np.mean(l1)
std1 = np.std(l1)

hyp1 = [m1-0.9*std1,m1+0.9*std1]
print(m1,std1)
pred1 = []
ac1 = []
for i in range(len(event)):
    if i not in r1:
        ac1.append('EVENT')
        if avg[event[i]]>hyp1[0] :
            pred1.append('EVENT')
        else:
            pred1.append('NONEVENT')   
            
for i in range(len(non_event)):
    if i not in r2:
        ac1.append('NONEVENT')
        if avg[non_event[i]]>hyp1[0] :
            pred1.append('EVENT')
        else:
            pred1.append('NONEVENT') 

from sklearn.metrics import confusion_matrix

con1 = confusion_matrix(ac1,pred1)
 
p1 = con1[0,0]/(con1[0,0]+con1[1,0])
re1 = con1[0,0]/(con1[0,0]+con1[0,1])
print(p1,re1)
print(2*p1*re1/(p1+re1))





m2 = np.mean(l2)
std2 = np.std(l2)
hyp2 = [m2-0.05*std2,m2+0.05*std2]
print(m2,std2)

pred2 = []
ac2 = []
for i in range(len(event)):
    if i not in r1:
        ac2.append('EVENT')
        if avg[event[i]]<hyp2[1]:
            pred2.append('NONEVENT')
        else:
            pred2.append('EVENT')   
            
for i in range(len(non_event)):
    if i not in r2:
        ac2.append('NONEVENT')
        if  avg[non_event[i]]<hyp2[1]:
            pred2.append('NONEVENT')
        else:
            pred2.append('EVENT') 

from sklearn.metrics import confusion_matrix

con2 = confusion_matrix(ac2,pred2)
p2 = con2[0,0]/(con2[0,0]+con2[1,0])
re2 = con2[0,0]/(con2[0,0]+con2[0,1])
print(p2,re2)
print(2*p2*re2/(p2+re2))



final = []
final.append(["Synch:","Annotation:","Avg Common Friends:"])

for i,j in annotations.items():
    final.append([i,j,avg[i]])
    
d = pd.DataFrame(final)
d.to_csv("Final_Data.csv",header=False)



