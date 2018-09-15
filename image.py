import cv2
import numpy as np

#path = 'images/0.jpg'
#path = 'images/1.jpg'
#path = 'images/2.jpg'   # somewhat works
#path = 'images/3.jpg'  # works
#path = 'images/5.jpg'
#path = 'images/6.jpg'
path = 'images/7.jpg'

img = cv2.imread(path)
img = cv2.resize(img,(600,400))
origImg = img.copy()
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#origImgGray = imgray.copy()
#imgray = cv2.GaussianBlur(imgray,(9,9),0)
thresh = cv2.Canny(imgray,100,200)
#ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)

# Morphology transform
kernel = np.ones((9,9),np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

img2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours,key = cv2.contourArea, reverse = True)[:5]


def fourCorners(cnt):
	peri = cv2.arcLength(cnt, True)
	approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
 
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		#screenCnt = approx
		cnt = approx
		print cv2.contourArea(cnt)
		X,Y,W,H = cv2.boundingRect(cnt)
		cv2.rectangle(origImg,(X,Y),(X+W,Y+H),(0,255,0),2)

		cv2.imshow('res',origImg)
		cv2.imshow('test',img2)
		cv2.waitKey(0)
	else:
		print 'No corners detected'

def slantCntDetect(cnt):
	rect = cv2.minAreaRect(cnt)
	box = cv2.boxPoints(rect)
	box = np.int0(box)
	cv2.drawContours(origImg,[box],0,(0,0,255),2)

	cv2.imshow('res',origImg)
	cv2.imshow('test',img2)
	cv2.waitKey(0)

def cntAreaDetect(cnt):
	#cv2.drawContours(origImg, [screenCnt], -1, (0, 255, 0), 2)
	print cv2.contourArea(cnt)
	X,Y,W,H = cv2.boundingRect(cnt)
	cv2.rectangle(origImg,(X,Y),(X+W,Y+H),(0,255,0),2)

	cv2.imshow('res',origImg)
	cv2.imshow('test',img2)
	cv2.waitKey(0)



for cnt in contours:
	# approximate the contour

	#fourCorners(cnt)
	cntAreaDetect(cnt)
	#slantCntDetect(cnt)

	

