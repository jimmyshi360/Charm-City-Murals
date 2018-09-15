import cv2
import numpy as np

# for wall
#path = 'wall-images/0.jpg' # works
#path = 'wall-images/1.jpg'
#path = 'wall-images/2.jpg' 
path = 'wall-images/3.jpg'   # 2nd mode works 
#path = 'wall-images/4.jpg'   # could use work
#path = 'wall-images/5.jpg'   # somewhat works
#path = 'wall-images/6.jpg'  # somewhat works   (uses 2nd mode)
#path = 'wall-images/7.jpg'   
#path = 'wall-images/8.jpg'   # could use work

img = cv2.imread(path)
img = cv2.resize(img,(600,400))
origImg = img.copy()

def getContours(img):
	img2, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours,key = cv2.contourArea, reverse = True)[:2]

	return contours

def imagePreprocess(img):
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#origImgGray = imgray.copy()
	#imgray = cv2.gaussianblur(imgray,(9,9),0)
	#ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)
	thresh = cv2.Canny(imgray,10,200)

	# Morphology transform
	kernel = np.ones((29,29),np.uint8)
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

	return thresh

def rectify(h):
	h = h.reshape((4,2))
	hnew = np.zeros((4,2),dtype = np.float32)

	add = h.sum(1)
	hnew[0] = h[np.argmin(add)]
	hnew[2] = h[np.argmax(add)]

	diff = np.diff(h,axis = 1)
	hnew[1] = h[np.argmin(diff)]
	hnew[3] = h[np.argmax(diff)]

	return hnew

def defineLineBounds(imgUse,cnt):
	# This code is for line fitting
	img = imgUse.copy()
	rows,cols = img.shape[:2]
	[vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
	lefty = int((-x*vy/vx) + y)
	righty = int(((cols-x)*vy/vx)+y)
	cv2.line(img,(cols-1,righty),(0,lefty),(255,0,0),2)


	
	# DEALING WITH UPPER BOUND
	imgT = imgUse.copy()[0:imgUse.shape[0]/2,0:imgUse.shape[1]]

	upperImg = imgT

	thresh = imagePreprocess(imgT)
	contours = getContours(thresh)

	rows,cols = imgT.shape[:2]
	[vx,vy,x,y] = cv2.fitLine(contours[0], cv2.DIST_L2,0,0.01,0.01)

	lefty = int((-x*vy/vx) + y)
	righty = int(((cols-x)*vy/vx)+y)

	upperRight = (cols-2, righty)
	upperLeft = (2,lefty)

	cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)




	# DEALING WITH LOWER BOUND

	lowerBound = imgUse.shape[0]/2

	imgT = imgUse.copy()[lowerBound:imgUse.shape[0],0:imgUse.shape[1]]
	lowerImg = imgT

	thresh = imagePreprocess(imgT)
	#imgray = cv2.cvtColor(imgT, cv2.COLOR_BGR2GRAY)
	#imgray = cv2.GaussianBlur(imgray,(9,9),0)
	#origImgGray = imgray.copy()
	#ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)

	lowerThresh = thresh

	contours = getContours(thresh)

	rows,cols = imgT.shape[:2]
	[vx,vy,x,y] = cv2.fitLine(contours[0], cv2.DIST_L2,0,0.01,0.01)

	lefty = int((-x*vy/vx) + y+lowerBound+100)
	righty = int(((cols-x)*vy/vx)+y+lowerBound+100)


	lowerRight = (cols-2, righty)
	lowerLeft = (2,lefty)

	cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)

	# Preform warp transform

	picWidth = origImg.shape[1]
	picHeight = origImg.shape[0]

	pts1 = np.float32([[upperLeft[0],upperLeft[1]],[upperRight[0],upperRight[1]],[lowerRight[0],lowerRight[1]],[lowerLeft[0],lowerLeft[1]]])
	pts2 = np.float32([[0,0],[picWidth,0],[picWidth,picHeight],[0,picHeight]])
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(origImg,M,(picWidth,picHeight))
	
	# Drawing closing lines
	cv2.line(img,upperLeft,lowerLeft,(0,255,0),2)
	cv2.line(img,upperRight,lowerRight,(0,255,0),2)



	#cv2.imshow('lowerThresh',thresh)
	#cv2.imshow('upper',upperImg)
	#cv2.imshow('lower',lowerImg)

	cv2.imshow('warped',dst)


	return img


def fourCorners(cnt):
	peri = cv2.arcLength(cnt, True)
	approx = cv2.approxPolyDP(cnt, 0.05 * peri, True)
 
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		#screenCnt = approx
		cnt = approx
		print cv2.contourArea(cnt)
		X,Y,W,H = cv2.boundingRect(cnt)
		#cv2.rectangle(origImg,(X,Y),(X+W,Y+H),(0,255,0),2)

		approxRec = rectify(approx)
		picHeight = origImg.shape[0]
		picWidth = origImg.shape[1]

		pts2 = np.float32([[0,0],[picWidth,0],[picWidth,picHeight],[0,picHeight]])
		M = cv2.getPerspectiveTransform(approxRec,pts2)
		dst = cv2.warpPerspective(origImg,M,(picWidth,picHeight))
		
		cv2.drawContours(origImg,[approx],0,(0,255,0),2)

		# This code is for line fitting
		rows,cols = img.shape[:2]
		[vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
		lefty = int((-x*vy/vx) + y)
		righty = int(((cols-x)*vy/vx)+y)
		cv2.line(origImg,(cols-1,righty),(0,lefty),(255,0,0),2)



		cv2.imshow('res',origImg)
		cv2.imshow('dst',dst)
		#cv2.imshow('test',img2)
		cv2.waitKey(0)
		
	else:
		print 'No corners detected'
		cnt = approx

		res = defineLineBounds(origImg,cnt)

		cv2.imshow('res',res)
		cv2.waitKey(0)


	return True


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
	cv2.drawContours(origImg, [cnt], -1, (0, 0, 255), 2)


	# Extreme points
	extLeft = tuple(cnt[cnt[:,:,0].argmin()][0])
	extRight = tuple(cnt[cnt[:,:,0].argmax()][0])
	extTop = tuple(cnt[cnt[:,:,1].argmin()][0])
	extBot = tuple(cnt[cnt[:,:,1].argmax()][0])

	cv2.circle(origImg, extLeft, 8, (0, 0, 255), -1)
	cv2.circle(origImg, extRight, 8, (0, 255, 0), -1)
	cv2.circle(origImg, extTop, 8, (255, 0, 0), -1)
	cv2.circle(origImg, extBot, 8, (255, 255, 0), -1)

	cv2.imshow('res',origImg)
	cv2.imshow('test',img2)
	cv2.waitKey(0)


thresh = imagePreprocess(img)
contours = getContours(thresh)

for cnt in contours:
	# approximate the contour

	if fourCorners(cnt):
		break
	#cntAreaDetect(cnt)
	#slantCntDetect(cnt)

	

