from __future__ import print_function
import cv2
from threading import Thread

import numpy as np
import imutils
from imutils.video import WebcamVideoStream
import bluetooth
import time

# import pykinect2
# from pykinect2 import PyKinectV2
# from pykinect2.PyKinectV2 import *
# from pykinect2 import PyKinectRuntime

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
        if (qx>rx and qx<(rx+rw)) or (rx>qx and rx<(qx+qw)):
            intersect_rect = q
            found = True

    if found:
        return [r, intersect_rect]
    else:
        return None

def get_strip(r, framewidth):
    rx, ry, rw, rh = r
    sect_len = int(framewidth/6)
    return 7-(int(rx/sect_len)+1)

def heartbeat(sock):
    try:
        sock.send("8Ag1")
        time.sleep(0.14)
        sock.send("8Ag2")
        time.sleep(0.14)
        sock.send("8Ag3")
        time.sleep(0.14)
        sock.send("8Ag3")
        time.sleep(0.14)
        sock.send("8Ag2")
        time.sleep(0.14)
        sock.send("8Ag1")
        time.sleep(0.14)

        sock.send("9Ab1")
        time.sleep(0.14)
        sock.send("9Ab2")
        time.sleep(0.14)
        sock.send("9Ab3")
        time.sleep(0.14)
        sock.send("9Ab3")
        time.sleep(0.14)
        sock.send("9Ab2")
        time.sleep(0.14)
        sock.send("9Ab1")
        time.sleep(0.14)
    except:
        pass

def transition(sock,prev,curr):
    try:
        sock.send(prev+"Xr1")
        time.sleep(0.14)
        sock.send(prev+"Xg3")
        time.sleep(0.14)
        sock.send(curr+"Xr3")
        time.sleep(0.14)
    except:
        pass

def plus1(sock):
    sock.send("7Ar1")
    time.sleep(0.8)
    sock.send("1Xb3")
    time.sleep(0.8)
    sock.send("7Ar1")
    time.sleep(0.8)
    sock.send("4Xb3")
    time.sleep(0.8)

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(sock,found_init_rect, img, rects, start_time, prevSect, prevRect=None, intersectRect=None, stasis=False, framewidth=0, thickness=1):
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
                try:
                    heartbeat(sock)
                    heartbeat(sock)
                    heartbeat(sock)
                    heartbeat(sock)
                    heartbeat(sock)
                    time.sleep(0.15)
                    start_time = time.time()
                except:
                    pass
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
            elapsed_time = time.time() - start_time
            #print elapsed_time
            #light up strip as person walks by, turn off prev lit strip
            if elapsed_time>0.15 and stasis==False:
                try:
                    currSect = str(get_strip(rects[0],framewidth))
                    if currSect != prevSect:
                        transition(sock,prevSect,currSect)

                    if np.rint(time.time())%10==0:
                        if np.rint(time.time())%200==0:
                            plus1(sock)
                            plus1(sock)
                            plus1(sock)
                            plus1(sock)
                            plus1(sock)
                        sock.send("7Xg3")
                        time.sleep(0.14)
                    sock.send(currSect + "X" + "r3")
                 
                    start_time = time.time()

                    prevSect = currSect
                except:
                    pass

        currRect = rects[0]
    return found_init_rect,currRect,intersectRect,stasis,start_time,prevSect


#------ MAIN ------------------------------------------------------------------------

target_name = "HC-06"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break
port = 1

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
#cap = cv2.VideoCapture('./sample data/test4.mp4')
cap = WebcamVideoStream(src=1).start()

count = 0
#if found, flash white and freeze on drawn for a bit. then clear and grab new one
found_init_rect = False
found_count = -1
stasis = False
prevRect = None
intersectRect = None
start_time = 0
sock = None

try:
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((target_address, port))
    sock.send("7Xg3")
    start_time = time.time()
except:
    pass

time.sleep(0.15)
start_time = time.time()
prevSect = '1'
socket_set_time = time.time()

while True:
    #ret,img = cap.read()
    img = cap.read()
    if (type(img) == type(None)):
        break
    else:
        framewidth = min(400, img.shape[1])
        img = imutils.resize(img, width=framewidth)
       
        # detect people in the image
        (found, weights) = hog.detectMultiScale(img, winStride=(4, 4),
    		padding=(8, 8), scale=1.05)
        
        if stasis==True and count-found_count>1:
            stasis = False
            found_count = -1
            intersectRect = None
            try:
                sock.send("7Xg3")
                start_time = time.time()
            except:
                pass
        #eval_time = time.time()
        found_init_rect,prevRect,intersectRect,stasis,start_time,prevSect = draw_detections(sock,found_init_rect,img,found,start_time,prevSect,prevRect,intersectRect,stasis,framewidth)
        #eval_time = time.time() - eval_time
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(img,str(eval_time),(10,25), font, 1,(255,255,255),2)
        cv2.imshow("Frame", img)

        count = count + 1
        if stasis == True and found_count==-1:
            found_count = count

    key = cv2.waitKey(1) & 0xFF


cap.stop()
cv2.destroyAllWindows()
sock.close()

#-----------------------KINECT-----------------------------------------
#NEW PLAN: launch c++ in parallel to write images to file in folder, delete after x secs, and imread python

# from cv2 import VideoWriter as writer
# from cv2 import VideoWriter_fourcc
# kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Body )
# fourcc = VideoWriter_fourcc(*"XVID")
# data = writer('x.avi', fourcc, 30.0, (1920,1080))
# count = 0
# while count < 20:
#     if kinect.has_new_color_frame():
#         frame = kinect.get_last_color_frame()
#         width = kinect.color_frame_desc.Width
#         height = kinect.color_frame_desc.Height
#         #data.write(frame.data())
#         if frame.data() is not None:
#             print frame.data()
#         count+=1
#         #print 'Width: ', width, 'Height', height
#         #cv2.imshow('kinect v2', frame.reshape(height*width,4))

# kinect.close()
# data.release()

# if __name__ == "__main__":

#     # Import package

#     import PyKinectTk

#     # Create connection to Kinect Service

#     App = PyKinectTk.Capture.KinectService(timeout=2)

#     # Start capturing data using auto-click

#     print "Listening for Kinect data"
    
#     App.listen(getVideo=True, Clicking=True)

#     # Add a meaningful name to the recording
    
#     name = raw_input("Would you like to name your recording? ")

#     App.NameRecording(name)

#     # Exit

#     raw_input("Recording saved as '%s', press Return to quit" % name)

#     App.close()