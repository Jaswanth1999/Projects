# Code was written by Jaswanth Reddy(17ucs074) and Jayanth Ede(17dcs003).


import cv2 as cv
import numpy as np

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
    


def dis(a,b):   # Calculates Equilidean Distance between Points in 2D space
    return (a[0]-b[0])**2+(a[1]-b[1])**2




def triangulate(im,tr): # Draws Triangles onto the Image(For viewing triangulation)
    le,br,_ = im.shape
    thr = 3
    
    img = im.copy()
    for p in tr:
        for i in range(3):
            for j in range(i+1,3):
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


def click_and_crop1(event, x, y, flags, param):     # Used to record the coordinates of Points selected by user on image 1.
	# grab references to the global variables
    global points1,points2
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
    if event == cv.EVENT_LBUTTONDOWN :
        points1.append((y,x))
        cv.rectangle(image1,(x,y),(x+2,y+2),(0,255,0),2)
        cv.imshow("image1", image1)
    
def click_and_crop2(event, x, y, flags, param):     # Used to record the coordinates of Points selected by user on image 2
	# grab references to the global variables
    global points1,points2
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
    if event == cv.EVENT_LBUTTONDOWN :
        points2.append((y,x))
        cv.rectangle(image2,(x,y),(x+2,y+2),(0,255,0),2)
        cv.imshow("image2", image2)
		
def affine_corresponding_pts(control_pts_list1,control_pts_list2,inter_control_pt,inter_pt):    #Calculates the Alpha and Beta values of points wihthin triangles formed by control points in Intermediate Image. Also returns the corresponding Affine Points in Source and Destination

    alpha=(((inter_control_pt[2][0]-inter_control_pt[0][0])*(inter_pt[1]-inter_control_pt[0][1]))-((inter_control_pt[2][1]-inter_control_pt[0][1])*(inter_pt[0]-inter_control_pt[0][0])))/(((inter_control_pt[1][1]-inter_control_pt[0][1])*(inter_control_pt[2][0]-inter_control_pt[0][0]))-((inter_control_pt[1][0]-inter_control_pt[0][0])*(inter_control_pt[2][1]-inter_control_pt[0][1])))
    
    beta=(((inter_control_pt[1][0]-inter_control_pt[0][0])*(inter_pt[1]-inter_control_pt[0][1]))-((inter_control_pt[1][1]-inter_control_pt[0][1])*(inter_pt[0]-inter_control_pt[0][0])))/(((inter_control_pt[1][0]-inter_control_pt[0][0])*(inter_control_pt[2][1]-inter_control_pt[0][1]))-((inter_control_pt[1][1]-inter_control_pt[0][1])*(inter_control_pt[2][0]-inter_control_pt[0][0])))
    
    x1=int(control_pts_list1[0][0]+(alpha*(control_pts_list1[1][0]-control_pts_list1[0][0]))+(beta*(control_pts_list1[2][0]-control_pts_list1[0][0])))
    y1=int(control_pts_list1[0][1]+(alpha*(control_pts_list1[1][1]-control_pts_list1[0][1]))+(beta*(control_pts_list1[2][1]-control_pts_list1[0][1])))

    x2=int(control_pts_list2[0][0]+(alpha*(control_pts_list2[1][0]-control_pts_list2[0][0]))+(beta*(control_pts_list2[2][0]-control_pts_list2[0][0])))
    y2=int(control_pts_list2[0][1]+(alpha*(control_pts_list2[1][1]-control_pts_list2[0][1]))+(beta*(control_pts_list2[2][1]-control_pts_list2[0][1])))

    tlist=[]
    
    tlist.append((x1,y1))   # Corresponding Affine Coordinates in Source
    tlist.append((x2,y2))   # Corresponding Affine Coordinates in Destination
    

    return tlist




def tri_morph(control_pts_list1,control_pts_list2,img1,img2,k,N):   #This function produces intermediate images


    b1,g1,r1=cv.split(img1)
    b2,g2,r2=cv.split(img2)

    r=img1.shape[0]
    c=img1.shape[1]

    temp_b=np.zeros([r,c])
    temp_g=np.zeros([r,c])
    temp_r=np.zeros([r,c])

    inter_control_pts=[]    #running for k

    for i in range(len(control_pts_list1)):
        temp1=((N-k)/N)*control_pts_list1[i][0] +(k/N)*control_pts_list2[i][0]
        temp2=((N-k)/N)*control_pts_list1[i][1] +(k/N)*control_pts_list2[i][1]

        inter_control_pts.append((int(temp1),int(temp2)))



    triangle_inter_pts_list=triangle_points(inter_control_pts[0],inter_control_pts[1],inter_control_pts[2]) # Points within triangle of Interframe


    for i in triangle_inter_pts_list:

        pts=affine_corresponding_pts(control_pts_list1,control_pts_list2,inter_control_pts,i)   #Source and Destination points
        
        temp_b[i[0],i[1]]=((N-k)/N)*b1[pts[0][0]][pts[0][1]] + (k/N)*b2[pts[1][0]][pts[1][1]]   #Color Interpolation
        temp_g[i[0],i[1]]=((N-k)/N)*g1[pts[0][0]][pts[0][1]] + (k/N)*g2[pts[1][0]][pts[1][1]]
        temp_r[i[0],i[1]]=((N-k)/N)*r1[pts[0][0]][pts[0][1]] + (k/N)*r2[pts[1][0]][pts[1][1]]


        
    res_img=cv.merge((temp_b,temp_g,temp_r))

    return res_img



print("Enter Number of Inter Frames to be generated\n")

k=int(input()) # K number of intermediate frames

N=k+1 # From Image0 to ImageN

print("Please Select Three Points each on Source and Destination Images respectively\n")
print("Please make sure you select the points on Second Image in the same order as selected for the First Image\n")

print("After satisfying yourself with the Triangulated Images Please close them to allow the next set of Instructions to run.......\n")


points1 = []
points2 = []
image1 = cv.imread("Bush.jpg")
image2 = cv.imread("Clinton.jpg")

clone1 = image1.copy()
clone2 = image2.copy()

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



# Delaunay Triangulation Approximation using OPENCV

max_border=image1.shape[0]
min_border=0

p1=[]
p1.extend([(0,0),(0,(max_border-1)),((max_border-1),0),((max_border-1),(max_border-1))])
for i in points1:
    p1.append(i)
subdiv1 = cv.Subdiv2D((0,0,max_border,max_border))
subdiv1.insert(p1)
triangles1 = subdiv1.getTriangleList()

p2=[]
borders = []
borders.extend([(0,0),(0,(max_border-1)),((max_border-1),0),((max_border-1),(max_border-1))])
p2.extend([(0,0),(0,(max_border-1)),((max_border-1),0),((max_border-1),(max_border-1))])
for i in points2:
    p2.append(i)
tr1=[]
tr2=[]

for i in triangles1:
    tlist1=[]    
    tlist1.append((int(i[0]),int(i[1])))
    tlist1.append((int(i[2]),int(i[3])))
    tlist1.append((int(i[4]),int(i[5])))
    
    tlist2=[]
    for r in tlist1:
        if r in borders:
             tlist2.append(r)
        else:
            for c in range(len(points1)):
                if r == points1[c]:
                    tlist2.append(points2[c])
    tr1.append(tlist1)
    tr2.append(tlist2)

triangulated1 = triangulate(image1,tr1)     #Draws Triangles on Image1
cv.imshow("befer1",triangulated1)

triangulated2 = triangulate(image2,tr2)     #Draws Traingles on Image2
cv.imshow("befer2",triangulated2)
cv.waitKey(0)


print("Please wait...... \n Generating Intermediate Images\n......\n........\n...........")


for j in range(-1,N):   # Running a loop to Generate 'k' number of Intermediate Frames

    temp_b=np.zeros([500,500])
    temp_g=np.zeros([500,500])
    temp_r=np.zeros([500,500])


    for i,k in zip(tr1,tr2):

        tlist1=[]
        
        tlist1.append(i[0])
        tlist1.append(i[1])
        tlist1.append(i[2])
        
        tlist2=[]
        
        tlist2.append(k[0])
        tlist2.append(k[1])
        tlist2.append(k[2])
    

        im=tri_morph(tlist1,tlist2,clone1,clone2,j+1,N) # Passing Source and Destination Control Points to tri_morph function.Also the Number of Intermediate frames are also passed.
        
        b,g,r=cv.split(im)

        temp_b=temp_b+b
        temp_g=temp_g+g
        temp_r=temp_r+r    

    result_img=cv.merge((temp_b,temp_g,temp_r))
    cv.imwrite('InterFrame'+str((j+1))+'.jpg',result_img)

print('\n.......Done')

