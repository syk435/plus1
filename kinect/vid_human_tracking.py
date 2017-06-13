import cv2
import numpy as np

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


#------ MAIN ------------------------------------------------------------------------

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
cap = cv2.VideoCapture('./sample data/test1.mp4')
count = 0
while cap.isOpened() and count < 200:
    ret,img = cap.read()
    found,w=hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
    draw_detections(img,found)
    if (type(img) == type(None)):
        break
    else:
        cv2.imshow('feed',img)
        #cv2.imshow('window-name',img)
    #cv2.imwrite("frame%d.jpg" % count, img)
    count = count + 1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()