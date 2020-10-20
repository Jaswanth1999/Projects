# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:39:24 2020

@author: jaswa
"""

import cv2 as cv;
import numpy as np;

def area_triangle(p1,p2,p3):
    area = p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1])
    if area<0:
        return -1*area/2
    else:
        return area/2

def triangle_points(p1,p2,p3):
    l = max([p1[0],p2[0],p3[0]])
    b = max([p1[1],p2[1],p3[1]])
    
    points = []
    area = area_triangle(p1,p2,p3)
    for i in range(l+1):
        for j in range(b+1):
            p=(i,j)
            a1 = area_triangle(p,p1,p2)
            a2 = area_triangle(p,p1,p3)
            a3 = area_triangle(p,p2,p3)
            
            if(area == a1+a2+a3):
                points.append(p)
            
    return points
    





def dis(a,b):
    return (a[0]-b[0])**2+(a[1]-b[1])**2




def triangulate(im,points):
    le,br,_ = im.shape
    p4 = (0,0)
    p5 = (le-1,0)
    p6 = (0,br-1)
    p7 = (le-1,br-1)
    thr = 3
    p = [points[0],points[1],points[2],p4,p5,p6,p7]
    max_dis=[]
    for i in range(7):
        di = []
        for j in range(7):
            di.append(dis(p[i],p[j]))
        max_dis.append(di.index(max(di)))
    
    img = im.copy()
    for i in range(7):
        for j in range(i+1,7):
            if(max_dis[i] == j):
                continue
            if(p[j][0] - p[i][0]==0):
                if p[j][1]>p[i][1]:
                    b1 = p[i][1]
                    b2 = p[j][1]
                else:
                    b2 = p[i][1]
                    b1 = p[j][1]
                for l in range(p[j][0],p[i][0]+1):
                     for b in range(b1,b2):
                         if(np.abs(l-p[i][0]) <= thr):
                             img[l,b,:] = 0
            else:
                if p[j][1]>p[i][1]:
                    b1 = p[i][1]
                    b2 = p[j][1]
                else:
                    b2 = p[i][1]
                    b1 = p[j][1]
                if p[j][0]>p[i][0]:
                    l1 = p[i][0]
                    l2 = p[j][0]
                else:
                    l2 = p[i][0]
                    l1 = p[j][0]
                m = (p[j][1] - p[i][1])/(p[j][0] - p[i][0])
                for l in range(l1,l2+1):
                    for b in range(b1,b2+1):
                        if(np.abs(b-p[i][1] - m*(l-p[i][0])) <= thr):
                            img[l,b,:] = 0
                            
    return img






def click_and_crop1(event, x, y, flags, param):
	# grab references to the global variables
    global points1,points2
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
    if event == cv.EVENT_LBUTTONDOWN :
        points1.append((y,x))
        cv.rectangle(image1,(x,y),(x+2,y+2),(0,255,0),2)
        cv.imshow("image1", image1)
    
def click_and_crop2(event, x, y, flags, param):
	# grab references to the global variables
    global points1,points2
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
    if event == cv.EVENT_LBUTTONDOWN :
        points2.append((y,x))
        cv.rectangle(image2,(x,y),(x+2,y+2),(0,255,0),2)
        cv.imshow("image2", image2)
		





points1 = []
points2 = []
image1 = cv.imread("Bush.jpg")
image2 = cv.imread("Clinton.jpg")

clone1 = image1.copy()
cv.namedWindow("image1")
cv.namedWindow("image2")

cv.setMouseCallback("image1", click_and_crop1)
cv.setMouseCallback("image2", click_and_crop2)

# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
    cv.imshow("image1", image1)
    cv.imshow("image2", image2)
    key = cv.waitKey(1) & 0xFF
	# if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image1 = clone1.copy()
    if(len(points1) == 3 and len(points2) == 3):
        cv.destroyAllWindows()
        break
	# if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        cv.destroyAllWindows()
        break


tr = triangulate(image1,points1)
cv.imshow("befer",tr)
cv.waitKey(0)







    