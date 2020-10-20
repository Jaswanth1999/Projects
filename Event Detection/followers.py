# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:57:53 2020

@author: jaswa
"""


import time
import tweepy
import pandas as pd
import numpy as np
import csv
import os


tokens = [['D90Wj06vC6VCScXDZlNFYoqbh','7f849ZJphmNfWw3YAnrvINsFASiYz1MEsFUHCCf6u87LgHDb1G','1236581224006561793-rXuXrxxE66fPAwdcBlWD6SV9eDuo7v','ibVvnNdJUVV5DUVfUm5e5N9Yk9HiwUbpkRoEslqnGVn0T'],
          ['rvtYVvwPtVcL68AZeo4lNSJit','yJQrdQWYO1bu6rUQhecQk5QEGF8ujR3un8zxG9Ff4ZvCftk4xr','1182899917943001088-1BuCJzSgnfFvmYyR2pNqq50L04jK6n','CZvLcPFGnllMPxfnapFjcEhCTRpw1WYfYuUAyO0Qbv71R'],
          ['iAgFGCVvYh05WDQJy7317PKVY','HAQBU056VGOfOhcqz8guvtscdLOnyGN1XdxoAGys5nsKjILDc7','1182901966411665413-BbdK04hrDJI4cEiYtcWtRyTeJbu7or','dmGjQ2TAul48OLLCPPD8s1sWm67Sv1rg4lcFIBGjQCMwh'],
          ["NrUofCSWl3QSlNYZRv19OmknH","3UY7qoQvMnRsplPbIJXy3SB4aD6kqPbjANV4cIZ9F7QGwGXFS0", "1268175907082039297-4u7gVk3c2zVZr14WJyO8kEAjaxIaPp","8ZkOwf0wq2Er0EDiVL5VA9UBW57oUh9XjMqf1AWS6ONkb"]]
tr=0
limit = 20
l = 0

def followers(iid):
    global tokens
    global tr
    global limit
    global l
    auth = tweepy.OAuthHandler(tokens[tr][0],tokens[tr][1])
    auth.set_access_token(tokens[tr][2],tokens[tr][3])

    api = tweepy.API(auth)
    #api.GetDirectMessages(return_json=True)
    ids=[]
    try:
        
        for page in tweepy.Cursor(api.friends_ids, user_id=iid).pages():
            x = page
            for i in x:
                ids.append(i)
    except tweepy.TweepError as ex:
      #  return ex
        if ex.reason == "Not authorized.":
            print(iid ,'not authorized so ignoring it','not autherized')
            l=0
            return [0]
        if ex.reason == "[{'code': 50, 'message': 'User not found.'}]" or ex.reason == "[{'code': 63, 'message': 'User has been suspended.'}]" or ex.reason == "[{'code': 34, 'message': 'Sorry, that page does not exist.'}]":
            print(iid ,'not authorized so ignoring it','User not found')
            l=0
            return [0]
        if ex.reason == "[{'message': 'Rate limit exceeded', 'code': 88}]":
            print(iid,tr,"Failed to run the command on that user, Retrying...",88)
            l+=1
            if l>=limit:
                l=0
                print('Limit Exceded so ignoring it')
                return [0]
            if tr == 3:
                tr=0
                return -1
            tr+=1
            return -1
        print(ex.reason)
        print(iid,print(len(ids)))
        return -1
            
    l=0
    return ids
'''
    ids = []
    for page in tweepy.Cursor(api.friends_ids, user_id=iid).pages():
        x = page
        time.sleep(60)

    return x
'''

path1 = 'D:\Proj\BTP\Followers'

path2 = 'D:\Proj\BTP\Friends_ICWSM'

path4 = 'D:\Proj\BTP\Errors_Followers'

path3 = 'D:\Proj\BTP\Error_Friends'




def common(l1,l2):
    count = 0
    for i in l1:
        if i in l2:
            count+=1
    return count

FILES = os.listdir("D:\Proj\BTP\Friends_ICWSM")
done = 48
c = 0
for skip in range(46,47):
    data = pd.read_csv('unique_users_ICWSM.csv',header=None,skiprows=skip,nrows=1)
    if data.values[0,0]+'.csv' in FILES:
        print("there")
        continue
    else:
        print(skip,data.values[0])
    length = data.shape[1]
    
    
    
    follower_dict = {}
    ids_index = {}
      
    
    for i in range(1,length):
        ids_index[data.values[0,i]] = i
        
    pos = 1    
    for ids in data.values[0,1:]:
        status = 0
        val = followers(ids)
        if val == [0]:
            continue
        elif val == -1:
            while val==-1:
                time.sleep(60)
                val = followers(ids)
            if val == [0]:
                continue
            follower_dict[ids] = val
            pos+=1
        else:                
            follower_dict[ids] = val
            pos+=1
            print(pos,',',end='')
            
        
    length = len(follower_dict.keys())
    u = list(follower_dict.keys())
    users = []
    users.append(data.values[0,0])
    for i in u:
        users.append(i)
    
    matrix = np.zeros([length,length]) -1
    for row in range(length-1):
        matrix[row+1,0] = users[row+1]
    for column in range(length-1):
        matrix[0,column+1] = users[column+1]
    
    for row in range(1,length):
        for col in range(1,length):
            if row == col:
                matrix[row,col] = 0
                continue
            if matrix[col,row] != -1:
                matrix[row,col] = matrix[col,row]
                continue

            id1 = users[row]
            id2 = users[col]
            matrix[row,col] = common(follower_dict[id1],follower_dict[id2])
    errs = []
    for i,j in follower_dict.items():
        if j==[0]:
            errs.append(i)
    e = pd.DataFrame(errs)
    e.to_csv(path3+'/'+data.values[0,0]+'.csv')
    d = pd.DataFrame(matrix)
    d.to_csv(path2+'/'+data.values[0,0]+'.csv')            
   # with open(path + '/unique_users.csv', mode='w',encoding='utf-8',newline='') as sd:
    #    sd_writer = csv.writer(sd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
FILES = os.listdir("D:\Proj\BTP\Friends_ICWSM")
        