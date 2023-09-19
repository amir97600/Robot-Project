/*
By downloading, copying, installing or using the software you agree to this
license. If you do not agree to this license, do not download, install,
copy or use the software.

                          License Agreement
               For Open Source Computer Vision Library
                       (3-clause BSD License)

Copyright (C) 2013, OpenCV Foundation, all rights reserved.
Third party copyrights are property of their respective owners.

Copyright (C) 2022, Adrien Boussicault 
  (made some modifications on the initial OpenCV Aruco examples)

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  * Neither the names of the copyright holders nor the names of the contributors
    may be used to endorse or promote products derived from this software
    without specific prior written permission.

This software is provided by the copyright holders and contributors "as is" and
any express or implied warranties, including, but not limited to, the implied
warranties of merchantability and fitness for a particular purpose are
disclaimed. In no event shall copyright holders or contributors be liable for
any direct, indirect, incidental, special, exemplary, or consequential damages
(including, but not limited to, procurement of substitute goods or services;
loss of use, data, or profits; or business interruption) however caused
and on any theory of liability, whether in contract, strict liability,
or tort (including negligence or otherwise) arising in any way out of
the use of this software, even if advised of the possibility of such damage.
*/


#include <opencv2/highgui.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/aruco/charuco.hpp>
#include <opencv2/imgproc.hpp>
#include <vector>
#include <iostream>
#include <ctime>

using namespace std;
using namespace cv;

namespace {
const char* about =
        "Calibration using a ChArUco board\n"
        "  To capture a frame for calibration, press 'c',\n"
        "  If input comes from video, press any key for next frame\n"
        "  To finish capturing, press 'ESC' key and calibration starts.\n";
const char* keys  =
  "{help     | false | Display help }"
  "{w        |       | Number of squares in X direction }"
  "{h        |       | Number of squares in Y direction }"
  "{sl       |       | Square side length (in meters) }"
  "{ml       |       | Marker side length (in meters) }"
  "{d        |       | dictionary: DICT_4X4_50=0, DICT_4X4_100=1, "
  "DICT_4X4_250=2, DICT_4X4_1000=3, DICT_5X5_50=4, DICT_5X5_100=5, "
  "DICT_5X5_250=6, DICT_5X5_1000=7, DICT_6X6_50=8, DICT_6X6_100=9, "
  "DICT_6X6_250=10, DICT_6X6_1000=11, DICT_7X7_50=12, DICT_7X7_100=13, "
  "DICT_7X7_250=14, DICT_7X7_1000=15, DICT_ARUCO_ORIGINAL = 16}"
  "{dp       |       | File of marker detector parameters }"
  "{rs       | false | Apply refind strategy }"
  "{zt       | false | Assume zero tangential distortion }"
  "{a        |       | Fix aspect ratio (fx/fy) to this value }"
  "{pc       | false | Fix the principal point at the center }"
  "{sc       | false | Show detected chessboard corners after calibration }"
  "{@videofile |<non> | Input video file }"
  "{@outfile |<none> | Output file with calibrated camera parameters }";
}

bool readDetectorParameters(
  string filename, Ptr<aruco::DetectorParameters> &params
){
    FileStorage fs(filename, FileStorage::READ);
    if(!fs.isOpened())
        return false;
    fs["adaptiveThreshWinSizeMin"] >> params->adaptiveThreshWinSizeMin;
    fs["adaptiveThreshWinSizeMax"] >> params->adaptiveThreshWinSizeMax;
    fs["adaptiveThreshWinSizeStep"] >> params->adaptiveThreshWinSizeStep;
    fs["adaptiveThreshConstant"] >> params->adaptiveThreshConstant;
    fs["minMarkerPerimeterRate"] >> params->minMarkerPerimeterRate;
    fs["maxMarkerPerimeterRate"] >> params->maxMarkerPerimeterRate;
    fs["polygonalApproxAccuracyRate"] >> params->polygonalApproxAccuracyRate;
    fs["minCornerDistanceRate"] >> params->minCornerDistanceRate;
    fs["minDistanceToBorder"] >> params->minDistanceToBorder;
    fs["minMarkerDistanceRate"] >> params->minMarkerDistanceRate;
    fs["cornerRefinementMethod"] >> params->cornerRefinementMethod;
    fs["cornerRefinementWinSize"] >> params->cornerRefinementWinSize;
    fs[
      "cornerRefinementMaxIterations"
    ] >> params->cornerRefinementMaxIterations;
    fs["cornerRefinementMinAccuracy"] >> params->cornerRefinementMinAccuracy;
    fs["markerBorderBits"] >> params->markerBorderBits;
    fs[
      "perspectiveRemovePixelPerCell"
    ] >> params->perspectiveRemovePixelPerCell;
    fs[
      "perspectiveRemoveIgnoredMarginPerCell"
    ] >> params->perspectiveRemoveIgnoredMarginPerCell;
    fs["maxErroneousBitsInBorderRate"] >> params->maxErroneousBitsInBorderRate;
    fs["minOtsuStdDev"] >> params->minOtsuStdDev;
    fs["errorCorrectionRate"] >> params->errorCorrectionRate;
    return true;
}

bool saveCameraParams(
  const string &filename, const Size & imageSize, float aspectRatio, int flags,
  const Mat &cameraMatrix, const Mat &distCoeffs, double totalAvgErr
){
    FileStorage fs(filename, FileStorage::WRITE);
    if(!fs.isOpened())
        return false;

    time_t tt;
    time(&tt);
    struct tm *t2 = localtime(&tt);
    char buf[1024];
    strftime(buf, sizeof(buf) - 1, "%c", t2);

    fs << "calibration_time" << buf;
    fs << "image_width" << imageSize.width;
    fs << "image_height" << imageSize.height;
    if(flags & CALIB_FIX_ASPECT_RATIO){
      fs << "aspectRatio" << aspectRatio;
    }
    if(flags != 0) {
      sprintf(
        buf, "flags: %s%s%s%s",
        flags & CALIB_USE_INTRINSIC_GUESS ? "+use_intrinsic_guess" : "",
        flags & CALIB_FIX_ASPECT_RATIO ? "+fix_aspectRatio" : "",
        flags & CALIB_FIX_PRINCIPAL_POINT ? "+fix_principal_point" : "",
        flags & CALIB_ZERO_TANGENT_DIST ? "+zero_tangent_dist" : ""
      );
    }
    fs << "flags" << flags;
    fs << "camera_matrix" << cameraMatrix;
    fs << "distortion_coefficients" << distCoeffs;
    fs << "avg_reprojection_error" << totalAvgErr;
    return true;
}

typedef struct {
    int squaresX;
    int squaresY;
    float squareLength;
    float markerLength;
    int dictionaryId;
    string outputFile;
    bool showChessboardCorners;
    int calibrationFlags;
    float aspectRatio;
    bool refindStrategy;
    String videoFile;
    Ptr<aruco::DetectorParameters> detectorParams;
} Parameters;

typedef enum {
  NO_ERROR = 0,
  NOT_ENOUGH_CAPTURES = 1,
  NOT_ENOUGHT_CORNERS = 2,
  FAIL_TO_SAVE_OUTPUT_FILE = 3,
  INVALID_NUMBER_OF_PARAMETERS = 4,
  PARAMETERS_FILE_CANT_BE_READEN = 5,
  PARAMETERS_ARE_NOT_VALID = 6
} Error_code;

int parse_command_line(Parameters & parameters, int argc, char *argv[]){
    CommandLineParser parser(argc, argv, keys);
    parser.about(about);

    if( (argc < 7) || parser.get<bool>("help") ) {
        parser.printMessage();
        return INVALID_NUMBER_OF_PARAMETERS;
    }

    parameters.squaresX = parser.get<int>("w");
    parameters.squaresY = parser.get<int>("h");
    parameters.squareLength = parser.get<float>("sl");
    parameters.markerLength = parser.get<float>("ml");
    parameters.dictionaryId = parser.get<int>("d");
    parameters.outputFile = parser.get<string>(1);
    parameters.showChessboardCorners = parser.get<bool>("sc");

    parameters.calibrationFlags = 0;
    parameters.aspectRatio = 1;
    if(parser.has("a")) {
        parameters.calibrationFlags |= CALIB_FIX_ASPECT_RATIO;
        parameters.aspectRatio = parser.get<float>("a");
    }
    if(parser.get<bool>("zt")){
      parameters.calibrationFlags |= CALIB_ZERO_TANGENT_DIST;
    }
    if(parser.get<bool>("pc")){
      parameters.calibrationFlags |= CALIB_FIX_PRINCIPAL_POINT;
    }

    parameters.detectorParams = aruco::DetectorParameters::create();
    if(parser.has("dp")) {
        bool readOk = readDetectorParameters(
          parser.get<string>("dp"), parameters.detectorParams
        );
        if(!readOk) {
            cerr << "Invalid detector parameters file" << endl;
            return PARAMETERS_FILE_CANT_BE_READEN;
        }
    }

    parameters.refindStrategy = parser.get<bool>("rs");
    parameters.videoFile = parser.get<string>(0);

    if(!parser.check()) {
        parser.printErrors();
        return PARAMETERS_ARE_NOT_VALID;
    }
    return NO_ERROR;
}

typedef struct {
  VideoCapture inputVideo;

  Ptr<aruco::Dictionary> dictionary;

  vector< vector< vector< Point2f > > > allCorners;
  vector< vector< int > > allIds;
  vector< Mat > allImgs;
  Size imgSize;

  vector< vector< Point2f > > allCornersConcatenated;
  vector< int > allIdsConcatenated;
  vector< int > markerCounterPerFrame;

} Aruco_data;

typedef struct {
    Ptr<aruco::CharucoBoard> charucoboard;
    Ptr<aruco::Board> board;

    vector< Mat > allCharucoCorners;
    vector< Mat > allCharucoIds;
    vector< Mat > filteredImages;
    vector< Mat > rvecs, tvecs;
} Charuco_data;

int extract_images_aruco_marker_and_it_corners_from_video(
  const Parameters& parameters, Aruco_data & aruco_data, 
  Charuco_data & charuco_data
){
  aruco_data.inputVideo.open(parameters.videoFile);
  aruco_data.dictionary = aruco::getPredefinedDictionary(
    aruco::PREDEFINED_DICTIONARY_NAME(parameters.dictionaryId)
  );
  charuco_data.charucoboard = aruco::CharucoBoard::create(
    parameters.squaresX, parameters.squaresY,
    parameters.squareLength, parameters.markerLength, aruco_data.dictionary
  );
  charuco_data.board = charuco_data.charucoboard.staticCast<aruco::Board>();

  // collect data from each frame
  while(aruco_data.inputVideo.grab()) {
      Mat image;
      aruco_data.inputVideo.retrieve(image);

      vector< int > ids;
      vector< vector< Point2f > > corners, rejected;

      aruco::detectMarkers(
        image, aruco_data.dictionary,  corners, ids, parameters.detectorParams, 
        rejected
      );

      if(parameters.refindStrategy){
        aruco::refineDetectedMarkers(
          image, charuco_data.board, corners, ids, rejected
        );
      }

      const int minimium_ids_number = 4;
      if(ids.size() >= minimium_ids_number) {
          aruco_data.allCorners.push_back(corners);
          aruco_data.allIds.push_back(ids);
          aruco_data.allImgs.push_back(image);
          aruco_data.imgSize = image.size();
      }
  }

  // prepare data for calibration
  aruco_data.markerCounterPerFrame.reserve(aruco_data.allCorners.size());
  for(unsigned int i = 0; i < aruco_data.allCorners.size(); i++) {
      aruco_data.markerCounterPerFrame.push_back(
        (int) aruco_data.allCorners[i].size()
      );
      for(unsigned int j = 0; j < aruco_data.allCorners[i].size(); j++) {
          aruco_data.allCornersConcatenated.push_back(
            aruco_data.allCorners[i][j]
          );
          aruco_data.allIdsConcatenated.push_back(aruco_data.allIds[i][j]);
      }
  }
  return NO_ERROR;
};

typedef struct {
    Mat cameraMatrix;
    Mat distCoeffs;
} Camera;

int extract_images_charuco_and_it_corners(
  const Aruco_data & aruco_data, Charuco_data & charuco_data, 
  const Camera & camera
){
  // prepare data for charuco calibration
  unsigned int nFrames = aruco_data.allCorners.size();
  charuco_data.allCharucoCorners.reserve(nFrames);
  charuco_data.allCharucoIds.reserve(nFrames);

  for(unsigned int i = 0; i < nFrames; i++) {
    // interpolate using camera parameters
    Mat currentCharucoCorners, currentCharucoIds;
    aruco::interpolateCornersCharuco(
      aruco_data.allCorners[i], aruco_data.allIds[i], aruco_data.allImgs[i],
      charuco_data.charucoboard, currentCharucoCorners, currentCharucoIds,
      camera.cameraMatrix, camera.distCoeffs
    );

    charuco_data.allCharucoCorners.push_back(currentCharucoCorners);
    charuco_data.allCharucoIds.push_back(currentCharucoIds);
    charuco_data.filteredImages.push_back(aruco_data.allImgs[i]);
  }
  return NO_ERROR;
}

void init_camera(const Parameters & parameters, Camera & camera){
    if(parameters.calibrationFlags & CALIB_FIX_ASPECT_RATIO) {
        camera.cameraMatrix = Mat::eye(3, 3, CV_64F);
        camera.cameraMatrix.at< double >(0, 0) = parameters.aspectRatio;
    }
}

int main(int argc, char *argv[]) {
    int error_code = NO_ERROR;
    Parameters parameters;
    Aruco_data aruco_data;
    Charuco_data charuco_data;
    Camera camera;

    error_code = parse_command_line(parameters, argc, argv);
    if( error_code ) return error_code;

    error_code = extract_images_aruco_marker_and_it_corners_from_video(
      parameters, aruco_data, charuco_data
    );
    if( error_code ) return error_code;
    
    if(aruco_data.allIds.size() < 1) {
        cerr << "The video don't contain enough captures for calibration" 
          << endl;
        return NOT_ENOUGH_CAPTURES;
    }

    init_camera(parameters, camera);

    // calibrate camera using only aruco markers
    double arucoRepErr;
    arucoRepErr = aruco::calibrateCameraAruco(
      aruco_data.allCornersConcatenated, aruco_data.allIdsConcatenated,
      aruco_data.markerCounterPerFrame, charuco_data.board, aruco_data.imgSize,
      camera.cameraMatrix, camera.distCoeffs, 
      noArray(), noArray(), 
      parameters.calibrationFlags
    );

    error_code = extract_images_charuco_and_it_corners(
      aruco_data, charuco_data, camera
    );
    if( error_code ) return error_code;

    if(charuco_data.allCharucoCorners.size() < 4) {
        cerr << "Not enough corners for calibration" << endl;
        return NOT_ENOUGHT_CORNERS;
    }

    // calibrate camera using only charuco
    double repError = aruco::calibrateCameraCharuco(
      charuco_data.allCharucoCorners, charuco_data.allCharucoIds, 
      charuco_data.charucoboard, aruco_data.imgSize,
      camera.cameraMatrix, camera.distCoeffs,
      charuco_data.rvecs, charuco_data.tvecs, parameters.calibrationFlags
    );

    bool saveOk = saveCameraParams(
      parameters.outputFile, aruco_data.imgSize, parameters.aspectRatio, 
      parameters.calibrationFlags, camera.cameraMatrix, camera.distCoeffs,
      repError
    );
    if(!saveOk) {
      cerr << "Cannot save output file" << endl;
      return FAIL_TO_SAVE_OUTPUT_FILE;
    }

    cout << "Re-projection Error for charuco : " << repError << endl;
    cout << "Re-projection Error for aruco: " << arucoRepErr << endl;
    cout << "Calibration saved to " << parameters.outputFile << endl;

    return error_code;
}
