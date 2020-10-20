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
		
def affine_corresponding_pts(control_pts_list1,control_pts_list2,inter_control_pt,inter_pt):

    alpha=(((inter_control_pt[2][0]-inter_control_pt[0][0])*(inter_pt[1]-inter_control_pt[0][1]))-((inter_control_pt[2][1]-inter_control_pt[0][1])*(inter_pt[0]-inter_control_pt[0][0])))/(((inter_control_pt[1][1]-inter_control_pt[0][1])*(inter_control_pt[2][0]-inter_control_pt[0][0]))-((inter_control_pt[1][0]-inter_control_pt[0][0])*(inter_control_pt[2][1]-inter_control_pt[0][1])))
    
    beta=(((inter_control_pt[1][0]-inter_control_pt[0][0])*(inter_pt[1]-inter_control_pt[0][1]))-((inter_control_pt[1][1]-inter_control_pt[0][1])*(inter_pt[0]-inter_control_pt[0][0])))/(((inter_control_pt[1][0]-inter_control_pt[0][0])*(inter_control_pt[2][1]-inter_control_pt[0][1]))-((inter_control_pt[1][1]-inter_control_pt[0][1])*(inter_control_pt[2][0]-inter_control_pt[0][0])))
    
    x1=int(control_pts_list1[0][0]+(alpha*(control_pts_list1[1][0]-control_pts_list1[0][0]))+(beta*(control_pts_list1[2][0]-control_pts_list1[0][0])))
    y1=int(control_pts_list1[0][1]+(alpha*(control_pts_list1[1][1]-control_pts_list1[0][1]))+(beta*(control_pts_list1[2][1]-control_pts_list1[0][1])))

    x2=int(control_pts_list2[0][0]+(alpha*(control_pts_list2[1][0]-control_pts_list2[0][0]))+(beta*(control_pts_list2[2][0]-control_pts_list2[0][0])))
    y2=int(control_pts_list2[0][1]+(alpha*(control_pts_list2[1][1]-control_pts_list2[0][1]))+(beta*(control_pts_list2[2][1]-control_pts_list2[0][1])))

    tlist=[]
    
    tlist.append((x1,y1))
    tlist.append((x2,y2))
    

    return tlist




def face_morph(control_pts_list1,control_pts_list2,img1,img2,k,N):   #This function produces intermediate images


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
        
        temp_b[i[0],i[1]]=((N-k)/N)*b1[pts[0][0]][pts[0][1]] + (k/N)*b2[pts[1][0]][pts[1][1]]
        temp_g[i[0],i[1]]=((N-k)/N)*g1[pts[0][0]][pts[0][1]] + (k/N)*g2[pts[1][0]][pts[1][1]]
        temp_r[i[0],i[1]]=((N-k)/N)*r1[pts[0][0]][pts[0][1]] + (k/N)*r2[pts[1][0]][pts[1][1]]


        
    res_img=cv.merge((temp_b,temp_g,temp_r))

    cv.imwrite('InterFrame'+str(k)+'.jpg',res_img)








k=4 # K number of intermediate frames

N=k+1 # From Image0 to ImageN

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


tr1 = triangulate(image1,points1)
cv.imshow("befer1",tr1)

tr2 = triangulate(image2,points2)
cv.imshow("befer2",tr2)



for i in range(-1,N):

    face_morph(points1,points2,image1,image2,i+1,N)



cv.waitKey(0)
p=[]
p.extend([(0,0),(0,499),(499,0),(499,499)])
for i in points1:
    p.append(i)
subdiv = cv.Subdiv2D((0,0,500,500))
subdiv.insert(p)
triangles = subdiv.getTriangleList()

        
        
