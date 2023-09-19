import cv2
import cv2.aruco as aruco
import numpy as np
import time

# input cam
video_capture = cv2.VideoCapture(2)
flag_img = 0 

while True : 
    if not video_capture.isOpened() :
        print("Camera not detected")

    key = cv2.waitKey(1)
    ret, frame = video_capture.read()
    # Display video
    cv2.imshow('Camera calibration', frame)
    
    if key == ord('s') :
        cv2.imwrite(f"./calibration_board_capture/capture_{flag_img}.png",frame)
        print(f'Image {flag_img} saved')
        flag_img += 1
        
        
    if key == ord('q') :
        print("End calibration")
        break
        
video_capture.release()
cv2.destroyAllWindows()