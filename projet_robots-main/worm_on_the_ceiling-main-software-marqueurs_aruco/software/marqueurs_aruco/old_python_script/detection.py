
import argparse
import cv2
import cv2.aruco as aruco
import numpy as np
import time
import imutils
from imutils.video import VideoStream
import calibration_charuco as cic
import json_functions as j

# Get matrix mtx and dist
data = j.load_json()
mtx = np.array(data['mtx'])
dist = np.array(data['dist'])



# Aruco dict
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

MARKER_SIZE = 100 #pix

# Generate 10 aruco markers
def generate_markers(aruco_dict, MARKER_SIZE) :
    for id_aruco in range(10):
        marker = aruco.drawMarker(aruco_dict,id_aruco,MARKER_SIZE)
        cv2.imwrite(f"markers/marker_{id_aruco}.png",marker)
# generate_markers(aruco_dict, MARKER_SIZE)


aruco_param = aruco.DetectorParameters_create()
aruco_param.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX


# Input video
capture_video0 = VideoStream("/dev/video2").start()
time.sleep(1)
capture_video1 = VideoStream("/dev/video0").start()
time.sleep(1)

while True : 
    
    frame0 = capture_video0.read()
    frame0 = imutils.resize(frame0,width=250)
    frame1 = capture_video1.read()    
    frame1 = imutils.resize(frame1,width=250)
    
    cam_0_1 = np.hstack((frame0, frame1)) # put videos in the same window
    
    # Detect markers    
    (aruco_corners, aruco_ID, rejected )= aruco.detectMarkers(
       cam_0_1, aruco_dict, parameters = aruco_param)
    
    (rvecs, tvecs,_) = aruco.estimatePoseSingleMarkers(aruco_corners, 0.019, mtx, dist)
    print("tvec : ", tvecs)
    print("##########")
    print("rvecs : ", rvecs)
    print("##########")
    if len(aruco_corners) > 0:
        aruco_ID = aruco_ID.flatten()
    
        for (markerCorner, markerId) in zip(aruco_corners, aruco_ID):
    
            corners_abcd = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners_abcd

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cv2.line(cam_0_1, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(cam_0_1, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(cam_0_1, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(cam_0_1, bottomLeft, topLeft, (0, 255, 0), 2)

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            
            cv2.circle(cam_0_1, (cX, cY), 4, (0, 0, 255), -1)
            
            cv2.circle(cam_0_1, (cX, cY), 4, (255, 0, 0), -1)
           
        
    if np.all(aruco_ID is not None):
        for i in range(0, len(aruco_ID)):
            cv2.drawFrameAxes(cam_0_1, mtx, dist, rvecs[i], tvecs[i],0.08)
        
    
    cv2.imshow('capture video cam 0 and 1',cam_0_1) # Show video
    if cv2.waitKey(1)== ord('q'): # Press q to quit
        break

cv2.destroyAllWindows()
capture_video0.stop()
capture_video1.stop()

