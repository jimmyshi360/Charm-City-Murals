import cv2
import numpy as np

#path = 'images/0.jpg'
#path = 'images/1.jpg'
path = 'images/2.jpg'   # somewhat works
#path = 'images/3.jpg'  # works
#path = 'images/5.jpg'
#path = 'images/6.jpg'
#path = 'images/7.jpg'

img = cv2.imread(path)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,200)

print lines

for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imshow('test',img)
cv2.waitKey(0)
