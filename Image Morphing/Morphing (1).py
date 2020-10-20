# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 21:27:37 2020

@author: susan
"""

import cv2 as cv
import numpy as np

src_c = [] # to store co-ordinates of control points in the source
dst_c = [] # to store co-ordinates of control points in the destination


def area_triangle(p1,p2,p3):
    area = p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1])
    if area<0:
        return -1*area/2
    else:
        return area/2

def triangle_points(p1,p2,p3):
    #finding limit till where we have to loop
    l = max([p1[0],p2[0],p3[0]])
    b = max([p1[1],p2[1],p3[1]])
    
    points = []
    area = area_triangle(p1,p2,p3)
    for i in range(int(l)+1):
        for j in range(int(b)+1):
            p=(i,j)
            a1 = area_triangle(p,p1,p2)
            a2 = area_triangle(p,p1,p3)
            a3 = area_triangle(p,p2,p3)
            
            if(area == a1+a2+a3):
                points.append(p)
            
    return points






# function to select the control points in the source image
def myfunc1(event,y,x,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        src_c.append((x,y))
        src_img[x-2:x+3,y-2:y+3] = (255,0,0)
        
# function to select the control points in the destination image
def myfunc2(event,y,x,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        dst_c.append((x,y))
        dst_img[x-2:x+3,y-2:y+3] = (0,0,255)

def triangulation(im,tr):
    #image length and bredth
    le,br,_ = im.shape
    #defines the thickness of the line
    thr = 3
    
    img = im.copy()
    #looping through every pair of point(edges) of all triangles 
    for p in tr:
        for i in range(3):
            for j in range(i+1,3):
                cv.line(img, tuple((p[i][1],p[i][0])), tuple((p[j][1],p[j][0])),(0,0,0))                            
                   
                            
    return img













## Start



print("Enter the number of intermediate frames to be generated\n")

print("click on three corresponding areas in the source & dest to be selected as the control points\n")


src_img = cv.imread('Bush.jpg')
dst_img = cv.imread('Clinton.jpg')

# creating copies of the images to be used in interpolation because original images will be triangulated
src_img1 = src_img.copy()
dst_img1 = dst_img.copy()

# create two windows
cv.namedWindow("Source")
cv.namedWindow("Destination")

# Step 1
# selecting control points by mouse clicks
cv.setMouseCallback("Source", myfunc1)
cv.setMouseCallback("Destination", myfunc2) 


while True:
    cv.imshow("Source", src_img)
    cv.imshow("Destination", dst_img)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
cv.destroyAllWindows()


# Step 2
# Delauny triangulation of source image
max_border = 500

lst1 = []
lst1.extend([(0,0),(0,(max_border-1)),((max_border-1),0),((max_border-1),(max_border-1))])
for i in src_c:
    lst1.append(i)
subdiv1 = cv.Subdiv2D((0,0,max_border,max_border))
subdiv1.insert(lst1)
tri_1 = subdiv1.getTriangleList()


#Corresponding triangles of destination image
lst2=[]
border_points_dst = []
border_points_dst.extend([(0,0),(0,(max_border-1)),((max_border-1),0),((max_border-1),(max_border-1))])
lst2.extend([(0,0),(0,(max_border-1)),((max_border-1),0),((max_border-1),(max_border-1))])
for i in dst_c:
    lst2.append(i)


# Sorting the triangles in the source in a certain order to help perform corresponding triangulation in destination image 
trg1=[]
trg2=[]

for i in tri_1:
    t_list1=[]    
    t_list1.append((int(i[0]),int(i[1])))
    t_list1.append((int(i[2]),int(i[3])))
    t_list1.append((int(i[4]),int(i[5])))
    
    t_list2=[]
    for r in t_list1:
        if r in border_points_dst:
             t_list2.append(r)
        else:
            for c in range(len(src_c)):
                if r == src_c[c]:
                    t_list2.append(dst_c[c])
    trg1.append(t_list1)
    trg2.append(t_list2)

#triangulated image of source image
triangulated1 = triangulation(src_img,trg1)
cv.imshow("befer1",triangulated1)
cv.waitKey(0)

#triangulated image of destination image image
triangulated2 = triangulation(dst_img,trg2)
cv.imshow("befer2",triangulated2)
cv.waitKey(0)

#if cv.waitKey(1) & 0xFF == ord("q"):
    #cv.destroyAllWindows()

N = 10
p1 = np.array(lst1[:])
p2 = np.array(lst2[:])
for k in range(1,N):
    p = ((N-k)/N)*p1 +  ((k)/N)*p2
    print(p)
    img = src_img.copy()
    for j in range(len(trg1)):
        tr1 = np.array(trg1[j])
        tr2 = np.array(trg2[j])
        tr = ((N-k)/N)*tr1 +  ((k)/N)*tr2
        points = triangle_points(tr[0],tr[1],tr[2])
        for i in points:
            alpha=(((tr[2][0]-tr[0][0])*(i[1]-tr[0][1]))-((tr[2][1]-tr[0][1])*(i[0]-tr[0][0])))/(((tr[1][1]-tr[0][1])*(tr[2][0]-tr[0][0]))-((tr[1][0]-tr[0][0])*(tr[2][1]-tr[0][1])))
    
            beta=(((tr[1][0]-tr[0][0])*(i[1]-tr[0][1]))-((tr[1][1]-tr[0][1])*(i[0]-tr[0][0])))/(((tr[1][0]-tr[0][0])*(tr[2][1]-tr[0][1]))-((tr[1][1]-tr[0][1])*(tr[2][0]-tr[0][0])))
            
            x1=int(tr1[0][0]+(alpha*(tr1[1][0]-tr1[0][0]))+(beta*(tr1[2][0]-tr1[0][0])))
            y1=int(tr1[0][1]+(alpha*(tr1[1][1]-tr1[0][1]))+(beta*(tr1[2][1]-tr1[0][1])))
        
            x2=int(tr2[0][0]+(alpha*(tr2[1][0]-tr2[0][0]))+(beta*(tr2[2][0]-tr2[0][0])))
            y2=int(tr2[0][1]+(alpha*(tr2[1][1]-tr2[0][1]))+(beta*(tr2[2][1]-tr2[0][1])))

            img[i] =  ((N-k)/N)*src_img[x1,y1] +  ((k)/N)*dst_img[x2,y2]
    cv.imwrite('Inter'+str(k)+'.jpg',img)
    


