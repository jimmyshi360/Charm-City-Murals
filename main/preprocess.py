import cv2
import numpy as np
import base64
import skimage.io

def getContours(img):
    img2, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key = cv2.contourArea, reverse = True)[:2]
    return contours

def imagePreprocess(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.Canny(imgray,100,200)

    # Morphology transform
    kernel = np.ones((9,9),np.uint8)
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

def defineLineBounds(origImg, imgUse,cnt):
    # This code is for line fitting
    img = imgUse.copy()
    rows,cols = img.shape[:2]
    [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((cols-x)*vy/vx)+y)
    '''
    cols = max(cols,1)
    righty = max(righty,0)
    lefty = max(lefty,0)
    '''
    cv2.line(img,(cols-1,righty),(0,lefty),(255,0,0),2)
    
    # DEALING WITH UPPER BOUND
    imgT = imgUse.copy()[0:imgUse.shape[0]/2,0:imgUse.shape[1]]

    upperImg = imgT

    thresh = imagePreprocess(imgT)
    contours = getContours(thresh)

    rows,cols = imgT.shape[:2]
    try:
        [vx,vy,x,y] = cv2.fitLine(contours[0], cv2.DIST_L2,0,0.01,0.01)
    except:
        vy = 2
        vx = 1
        y = int(imgT.shape[1]*0.75)
        x = 1
    
    if abs(vy/vx) > 1.0:
        mulVal = 0
    else:
        mulVal = vy/vx

    lefty = int((-x*mulVal) + y)
    righty = int(((cols-x)*mulVal)+y)

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

    try:
        [vx,vy,x,y] = cv2.fitLine(contours[0], cv2.DIST_L2,0,0.01,0.01)
    except:
        vy = 2
        vx = 1
        y = int(imgT.shape[1]*0.75)
        x = 1

    '''
    lefty = int((-x*vy/vx) + y+lowerBound+100)
    righty = int(((cols-x)*vy/vx)+y+lowerBound+100)
    '''

    if abs(vy/vx) > 1.0:
        mulVal = 0
    else:
        mulVal = vy/vx
        

    lefty = int((-x*mulVal) + y+lowerBound)
    righty = int(((cols-x)*mulVal)+y+lowerBound)

        

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


    return img, [upperLeft, upperRight,lowerRight,lowerLeft]

def normalizeBB(shapeAR,box):
    resList = []
    print shapeAR.shape
    xSh,ySh,_ = shapeAR.shape

    for coord in box:
        
        x = coord[0]*(xSh/480.0)
        y = coord[1]*(ySh/640.0)

        resList.append((x,y))
    return resList

def fourCorners(img, origImg, cnt):
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.05 * peri, True)
 
    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    if len(approx) == 4:
        #screenCnt = approx
        cnt = approx
        print cv2.contourArea(cnt)
        X,Y,W,H = cv2.boundingRect(cnt)

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

        bbox = cv2.minAreaRect(approx)
        pts = cv2.boxPoints(bbox).astype(int)
        lowerLeft = (pts[0][0],pts[0][1])
        upperLeft = (pts[1][0],pts[1][1])
        upperRight = (pts[2][0],pts[2][1])
        lowerRight = (pts[3][0],pts[3][1])

        boundingBox = [upperLeft, upperRight,lowerRight,lowerLeft]
 
    else:
        print 'No corners detected'
        cnt = approx*48

        res, boundingBox = defineLineBounds(origImg, origImg,cnt)

    boundingBox = normalizeBB(origImg,boundingBox)
    return res, boundingBox

def decode(base64_string):
    if isinstance(base64_string, bytes):
        base64_string = base64_string.decode("utf-8")

    imgdata = base64.b64decode(base64_string)
    img = skimage.io.imread(imgdata, plugin='imageio')
    return img

def getPointsOfMural(imgStr):
    img = decode(imgStr)

    thresh = imagePreprocess(img)
    contours = getContours(thresh)
    origImg = img.copy()

    for cnt in contours:
        # approximate the contour
        print 'Entering'
        res,boundingBox = fourCorners(img, origImg, cnt)

        res = cv2.cvtColor(res, cv2.COLOR_BGRA2BGR) 
        res = cv2.resize(res,(1000,1000))
        res = np.reshape(res, [1,1000,1000,3])
        print boundingBox

        return res, boundingBox
    return None, None
