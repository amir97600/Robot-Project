"""
Fait avec la doc opencv
"""
import cv2
import cv2.aruco as aruco
import glob
import numpy as np 
import json_functions as j

mm = 0.0001
squaresX = 7
squaresY = 5
squareLenght = 28.15 * mm
markerLenght = 22.53 * mm

charuco_image_width = 1000
charuco_image_height = 1000

charuco_board_path = "./calibration/charuco_board.png"
charuco_directory = "./calibration_board_capture/"
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

def generate_charuco_board_calibration(aruco_dict):

	charuco_board = aruco.CharucoBoard_create(squaresX, squaresY, squareLenght, markerLenght, aruco_dict)
	print(type(charuco_board))
	im = charuco_board.draw((charuco_image_width, charuco_image_height))
	cv2.imwrite(charuco_board_path,im)

	return charuco_board

def read_chessboards():
	
	print("POSE ESTIMATION STARTS:")
	images = glob.glob(charuco_directory+"*.png")
	images = np.array(images)

	board = generate_charuco_board_calibration(aruco_dict)
	
	allCorners = []
	allIds = []
	decimator = 0
	epsilon = 0.00001
	max_count = 100
	
	# SUB PIXEL CORNER DETECTION CRITERION
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_count, epsilon)
	
	for im in images:
		print("=> Processing image {0}".format(im))
		frame = cv2.imread(im)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)
		
		if len(corners)>0:
			# SUB PIXEL DETECTION
			for corner in corners:
				
				cv2.cornerSubPix(gray, corner,
									winSize = (3,3),
									zeroZone = (-1,-1),
									criteria = criteria)

			res2 = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, board)
			
			if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
				allCorners.append(res2[1])
				allIds.append(res2[2])

		decimator+=1

	imsize = gray.shape
	return allCorners,allIds,imsize

def calibrate_camera(allCorners,allIds,imsize):

	cm = 0.01
	width_rectangle = 13 * cm
	height_rectangle = 10 * cm
	z_pos_rectangle = 17 * cm
	width_img = imsize[1]
	height_img = imsize[0]
	print("imsize : ",imsize)
	fx = width_img * z_pos_rectangle / width_rectangle
	fy = height_img * z_pos_rectangle / height_rectangle

	print("fx : ",fx)
	print("#########")
	print("fy : ",fy)
	cameraMatrixInit = np.array([[ fx,    0., width_img/2.],
                                 [    0., fy, height_img/2.],
                                 [    0.,    0.,           1.]])
	distCoeffsInit = np.zeros((5,1))
	flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)


	(ret, camera_matrix, distortion_coefficients0,
	rotation_vectors, translation_vectors,
	stdDeviationsIntrinsics, stdDeviationsExtrinsics,
	perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
					charucoCorners=allCorners,
					charucoIds=allIds,
					board=generate_charuco_board_calibration(aruco_dict),
					imageSize=imsize,
					cameraMatrix=cameraMatrixInit,
					distCoeffs=distCoeffsInit,
					flags=flags,
					criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

	return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors
	
allCorners,allIds,imsize=read_chessboards()
ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners,allIds,imsize)

print(mtx)
save = (mtx,dist)
j.write_json(save)



