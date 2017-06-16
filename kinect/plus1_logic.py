import cv2
import numpy as np
import imutils

def get_init_largest_rect(rects):
    maxSize = 0
    closestRectToCamera = []
    if len(rects) > 0:
        for x, y, w, h in rects:
            if w*h > maxSize:
                maxSize = w*h
                closestRectToCamera = [x, y, w, h]
        return [np.array(closestRectToCamera)]
    else:
        return None

def get_closest_rect(rects, prevRect):
    minDiff = 1000000
    closestRect = []
    if len(rects) > 0:
        for x, y, w, h in rects:
            diff = ((prevRect[0]-x)**2 + (prevRect[1]-y)**2)**0.5
            if diff < minDiff:
                minDiff = diff
                closestRect = [x, y, w, h]
        #print minDiff
        return [np.array(closestRect)]
    else:
        return [prevRect]

def get_intersect_rect(r, rects):
    #check x,y and later check depth
    #how to avoid recaputring same group? especially if they stop in front and look/talk?
    intersect_rect = []
    found = False
    rx, ry, rw, rh = r
    for q in rects:
        qx, qy, qw, qh = q
        if (qx>rx and qx<(rx+rw) and abs(qy-ry)<4) or (rx>qx and rx<(qx+qw) and abs(qy-ry)<4):
            intersect_rect = q
            found = True

    if found:
        return [r, intersect_rect]
    else:
        return None

def get_strip(r, framewidth):
    pass

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(found_init_rect, img, rects, prevRect=None, intersectRect=None, stasis=False, thickness=1):
    currRect = None
    if stasis==False:
        if found_init_rect:
            full_rects = rects
            rects = get_closest_rect(rects, prevRect)
            inter_rects = get_intersect_rect(rects[0], full_rects)
            if inter_rects is not None:
                found_init_rect = False
                stasis = True
                rects = inter_rects
                intersectRect = rects[1]
                #FLASH WHITE
        else:
            rects = get_init_largest_rect(rects)
            if rects is not None:
                found_init_rect = True
    else:
        rects = [prevRect,intersectRect]

    if rects is not None:
        for x, y, w, h in rects:
            pad_w, pad_h = int(0.15*w), int(0.05*h)
            cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

        currRect = rects[0]
    return found_init_rect,currRect,intersectRect,stasis


#------ MAIN ------------------------------------------------------------------------

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
cap = cv2.VideoCapture('./sample data/test3.mp4')
count = 0
#if found, flash white and freeze on drawn for a bit. then clear and grab new one
found_init_rect = False
found_count = -1
stasis = False
prevRect = None
intersectRect = None

while cap.isOpened():# and count < 100:
    ret,img = cap.read()
    if (type(img) == type(None)):
        break
    else:
        framewidth = min(400, img.shape[1])
        img = imutils.resize(img, width=framewidth)
       
        # detect people in the image
        (found, weights) = hog.detectMultiScale(img, winStride=(4, 4),
    		padding=(8, 8), scale=1.05)
        
        if stasis==True and count-found_count>50:
            stasis = False
            found_count = -1
            intersectRect = None

        found_init_rect,prevRect,intersectRect,stasis = draw_detections(found_init_rect,img,found,prevRect,intersectRect,stasis)
        cv2.imshow('Person detection',img)

        count = count + 1
        if stasis == True and found_count==-1:
            found_count = count
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()