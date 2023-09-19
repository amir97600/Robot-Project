cmake_minimum_required(VERSION 2.8)

project( camera_calibration_with_aruco )

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror -ggdb")

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( display_image display_image.cpp )
target_link_libraries( display_image ${OpenCV_LIBS} )

add_executable( calibrate_camera_charuco calibrate_camera_charuco.cpp )
target_link_libraries( calibrate_camera_charuco  ${OpenCV_LIBS} )

add_executable( capture_video capture_video.cpp )
target_link_libraries( capture_video ${OpenCV_LIBS} )

add_executable( concatenate_videos concatenate_videos.cpp )
target_link_libraries( concatenate_videos ${OpenCV_LIBS} )

add_executable( create_aruco_board create_aruco_board.cpp )
target_link_libraries( create_aruco_board ${OpenCV_LIBS} )

add_executable( create_aruco_diamond create_aruco_diamond.cpp )
target_link_libraries( create_aruco_diamond ${OpenCV_LIBS} )

add_executable( create_aruco_marker create_aruco_marker.cpp )
target_link_libraries( create_aruco_marker ${OpenCV_LIBS} )

add_executable( create_charuco_board create_charuco_board.cpp )
target_link_libraries( create_charuco_board ${OpenCV_LIBS} )

add_executable( create_grid_of_aruco_to_cut_out create_grid_of_aruco_to_cut_out.cpp )
target_link_libraries( create_grid_of_aruco_to_cut_out ${OpenCV_LIBS} )

add_executable( detect_aruco_markers detect_aruco_markers.cpp )
target_link_libraries( detect_aruco_markers ${OpenCV_LIBS} )
