# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 17:10:21 2020

@author: jaswa
"""

import cv2
import numpy as np
import glob
import os
 
img_array = []
f_name = []
os.chdir('D:\Proj\MPA\Images')
for i in range(3,101):
    filename = 'InterFrame'+str(i)+'.jpg'
    f_name.append(filename)
    img = cv2.imread(filename)
    i = cv2.medianBlur(img,ksize = 3)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(i)
 
 
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()