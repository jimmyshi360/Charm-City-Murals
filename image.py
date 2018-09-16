import cv2
import numpy as np

# For mural
#path = 'images/paper.jpg'
#path = 'images/0.jpg'   # works
#path = 'images/1.jpg'   # works
#path = 'images/2.jpg'   # somewhat works
path = 'images/3.jpg'  # works
#path = 'images/5.jpg'
#path = 'images/6.jpg'   
#path = 'images/7.jpg'   # works
#path = 'images/8.jpg'
#path = 'images/9.jpg'
#path = 'images/11.jpg'   # somewhat works
#path = 'images/12.jpg'    # works just a litle bit
#path = 'images/13.jpg'
#path = 'images/14.jpg'
#path = 'images/15.jpg'
#path = 'images/16.jpg'   
#path = 'images/17.jpg'     # works 


#path = 'images/5.jpg'    # could use some work
font = cv2.FONT_HERSHEY_SIMPLEX


img = cv2.imread(path)
img = cv2.resize(img,(600,400))
origImg = img.copy()
globalThresh = None

def getContours(img):
	img2, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours,key = cv2.contourArea, reverse = True)[:2]

	return contours

def imagePreprocess(img):
	global globalThresh
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	thresh = cv2.Canny(imgray,100,200)
	#thresh = cv2.Canny(imgray,10,200)

	# Morphology transform
	kernel = np.ones((9,9),np.uint8)
	#kernel = np.ones((29,29),np.uint8)
	#kernel = np.ones((15,15),np.uint8)
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

	globalThresh = thresh

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

	lowerThresh = thresh

	contours = getContours(thresh)

	rows,cols = imgT.shape[:2]
	[vx,vy,x,y] = cv2.fitLine(contours[0], cv2.DIST_L2,0,0.01,0.01)

	'''
	lefty = int((-x*vy/vx) + y+lowerBound+100)
	righty = int(((cols-x)*vy/vx)+y+lowerBound+100)
	'''
	lefty = int((-x*vy/vx) + y+lowerBound)
	righty = int(((cols-x)*vy/vx)+y+lowerBound)

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



	cv2.imshow('lowerThresh',thresh)
	#cv2.imshow('upper',upperImg)
	#cv2.imshow('lower',lowerImg)

	cv2.imshow('warped',dst)


	return img, [upperLeft, upperRight,lowerRight,lowerLeft]


def fourCorners(cnt):
	global globalThresh
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
		#cv2.line(origImg,(cols-1,righty),(0,lefty),(255,0,0),2)

		res = origImg.copy()

		cv2.imshow('dst',dst)
		cv2.imshow('globe',globalThresh)
	
		bbox = cv2.minAreaRect(approx)
		pts = cv2.boxPoints(bbox).astype(int)
		lowerLeft = (pts[0][0],pts[0][1])
		upperLeft = (pts[1][0],pts[1][1])
		upperRight = (pts[2][0],pts[2][1])
		lowerRight = (pts[3][0],pts[3][1])

		boundingBox = [upperLeft, upperRight,lowerRight,lowerLeft]
	
	else:
		print 'No corners detected'
		cnt = approx

		res, boundingBox = defineLineBounds(origImg,cnt)

		
	print boundingBox

	textWrite = 'This is Mural A'
        cv2.putText(res,textWrite,(10,40),font,1,(255,255,255),1,cv2.LINE_AA)
	cv2.imshow('res',res)
	cv2.waitKey(0)


	return boundingBox



def getPointsOfMural():
	thresh = imagePreprocess(img)
	contours = getContours(thresh)

	for cnt in contours:
		# approximate the contour

		return fourCorners(cnt)
		

	

#getPointsOfMural()
