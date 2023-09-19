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
  "Capture images to be used to camera calibration.\n"
  "  Capture a frame for calibration, press 'c',\n"
  "  If input comes from video, press any key for next frame\n"
  "  To finish capturing, press 'ESC' key a video with selected frame will be\n"
  "  created.\n";
const char* keys  =
  "{w        |       | Number of squares in X direction }"
  "{h        |       | Number of squares in Y direction }"
  "{sl       |       | Square side length (in meters) }"
  "{ml       |       | Marker side length (in meters) }"
  "{d        |       | dictionary: DICT_4X4_50=0, DICT_4X4_100=1, "
  "DICT_4X4_250=2, DICT_4X4_1000=3, DICT_5X5_50=4, DICT_5X5_100=5, "
  "DICT_5X5_250=6, DICT_5X5_1000=7, DICT_6X6_50=8, DICT_6X6_100=9, "
  "DICT_6X6_250=10, DICT_6X6_1000=11, DICT_7X7_50=12, DICT_7X7_100=13, "
  "DICT_7X7_250=14, DICT_7X7_1000=15, DICT_ARUCO_ORIGINAL = 16}"
  "{@outfile |<none> | Output file with calibrated camera parameters }"
  "{ci       | 0     | Camera id if input doesnt come from video (-v) }"
  "{v        |       | Input video file, if ommited, input comes from camera }"
  "{dp       |       | File of marker detector parameters }"
  "{rs       | false | Apply refind strategy }";
}

static bool readDetectorParameters(
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
  fs["cornerRefinementMaxIterations"] >> params->cornerRefinementMaxIterations;
  fs["cornerRefinementMinAccuracy"] >> params->cornerRefinementMinAccuracy;
  fs["markerBorderBits"] >> params->markerBorderBits;
  fs["perspectiveRemovePixelPerCell"] >> params->perspectiveRemovePixelPerCell;
  fs[
    "perspectiveRemoveIgnoredMarginPerCell"
  ] >> params->perspectiveRemoveIgnoredMarginPerCell;
  fs["maxErroneousBitsInBorderRate"] >> params->maxErroneousBitsInBorderRate;
  fs["minOtsuStdDev"] >> params->minOtsuStdDev;
  fs["errorCorrectionRate"] >> params->errorCorrectionRate;
  return true;
}

typedef struct {
    int squaresX;
    int squaresY;
    float squareLength;
    float markerLength;
    int dictionaryId;
    Ptr<aruco::DetectorParameters> detectorParams;
    Ptr<aruco::Dictionary> dictionary;
    Ptr<aruco::CharucoBoard> charucoboard;
    Ptr<aruco::Board> board;

    bool refindStrategy;
} Charuco_data;

typedef struct {
    string input_video;
    int camId;
    VideoCapture video_capture;
    int waitTime;

    string outputFile;
} Video_data;

typedef enum {
  NO_ERROR = 0,
  NOT_ENOUGH_CAPTURES = 1,
  NOT_ENOUGHT_CORNERS = 2,
  FAIL_TO_SAVE_OUTPUT_FILE = 3,
  INVALID_NUMBER_OF_PARAMETERS = 4,
  PARAMETERS_FILE_CANT_BE_READEN = 5,
  PARAMETERS_ARE_NOT_VALID = 6
} Error_code;

int parse_command_line(
  Charuco_data & charuco_data, Video_data & video_data, 
  int argc, char *argv[]
){
    CommandLineParser parser(argc, argv, keys);
    parser.about(about);

    if(argc < 7) {
        parser.printMessage();
        return INVALID_NUMBER_OF_PARAMETERS;
    }
    
    charuco_data.squaresX = parser.get<int>("w");
    charuco_data.squaresY = parser.get<int>("h");
    charuco_data.squareLength = parser.get<float>("sl");
    charuco_data.markerLength = parser.get<float>("ml");
    charuco_data.dictionaryId = parser.get<int>("d");

    video_data.outputFile = parser.get<string>(0);
    
    charuco_data.detectorParams = aruco::DetectorParameters::create();
    if(parser.has("dp")) {
        bool readOk = readDetectorParameters(
          parser.get<string>("dp"), charuco_data.detectorParams
        );
        if(!readOk) {
            cerr << "Invalid detector parameters file" << endl;
            return 0;
        }
    }

    charuco_data.refindStrategy = parser.get<bool>("rs");
    video_data.camId = parser.get<int>("ci");

    video_data.input_video = parser.get<string>("v");

    if(!parser.check()) {
        parser.printErrors();
        return PARAMETERS_ARE_NOT_VALID;
    }
  return NO_ERROR;
}

void initialize_charuco_data(Charuco_data & charuco_data){
    charuco_data.dictionary = aruco::getPredefinedDictionary(
      aruco::PREDEFINED_DICTIONARY_NAME(charuco_data.dictionaryId)
    );

    // create charuco board object
    charuco_data.charucoboard = aruco::CharucoBoard::create(
      charuco_data.squaresX, charuco_data.squaresY, 
      charuco_data.squareLength, charuco_data.markerLength, 
      charuco_data.dictionary
    );
    charuco_data.board = charuco_data.charucoboard.staticCast<aruco::Board>();
}

void initialize_video_capture(Video_data & video_data){
  if(! video_data.input_video.empty()) {
    video_data.video_capture.open(video_data.input_video);
    video_data.waitTime = 0;
  } else {
    video_data.video_capture.open(video_data.camId);
    video_data.waitTime = 10;
  }
}

int main(int argc, char *argv[]) {
    int error_code = NO_ERROR;
    Charuco_data charuco_data;
    Video_data video_data;

    error_code = parse_command_line(charuco_data, video_data, argc, argv);
    if( error_code ) return error_code;

    initialize_charuco_data(charuco_data);
    initialize_video_capture(video_data);

    // collect data from each frame
    vector< vector< int > > allIds;
    vector< Mat > allImgs;
    Size imgSize;

    while(video_data.video_capture.grab()) {
        Mat image, imageCopy;
        video_data.video_capture.retrieve(image);

        vector< int > ids;
        vector< vector< Point2f > > corners, rejected;

        // detect markers
        aruco::detectMarkers(
          image, charuco_data.dictionary, corners, ids, 
          charuco_data.detectorParams, rejected
        );

        // refind strategy to detect more markers
        if(charuco_data.refindStrategy){
          aruco::refineDetectedMarkers(
            image, charuco_data.board, corners, ids, rejected
          );
        }

        // interpolate charuco corners
        Mat currentCharucoCorners, currentCharucoIds;
        if(ids.size() > 0){
          aruco::interpolateCornersCharuco(
            corners, ids, image,
            charuco_data.charucoboard, currentCharucoCorners,
            currentCharucoIds
          );
        }

        // draw results
        image.copyTo(imageCopy);
        if(ids.size() > 0){
          aruco::drawDetectedMarkers(imageCopy, corners);
        }

        if(currentCharucoCorners.total() > 0){
          aruco::drawDetectedCornersCharuco(
            imageCopy, currentCharucoCorners, currentCharucoIds
          );
        }

        putText(
          imageCopy,
          "Press 'c' to add current frame. 'ESC' to save images in a video.",
          Point(10, 20), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(255, 0, 0), 2
        );

        imshow("out", imageCopy);

        char key = (char)waitKey(video_data.waitTime);
        if(key == 27) break;
        if(key == 'c'){
          const unsigned int minimal_aruco_number = 4;
          if(ids.size() < minimal_aruco_number){
            cout << "There is not enought aruco markers in that image." 
                 << std::endl;
            cout << "At least " << minimal_aruco_number << " markers are "
                 << "needed." << std::endl;;
            cout << "Frame is not captured." << endl;
            continue;
          }
          cout << "Frame captured" << endl;
          allIds.push_back(ids);
          allImgs.push_back(image);
          imgSize = image.size();
        }
    }

    // Save the images inside a video
    const int frame_per_second = 10;
    cv::VideoWriter video_writer(
      video_data.outputFile,

      //Without loss of informations
      //cv::VideoWriter::fourcc('L', 'A', 'G', 'S'),
      cv::VideoWriter::fourcc('F', 'F', 'V', '1'),

      // with loss of informations
      // VideoWriter::fourcc('M','J','P','G'), 

      frame_per_second, imgSize
    );
    for(unsigned int i=0; i< allImgs.size(); i++ ){
      video_writer.write(allImgs[i]);
    }

    if(allIds.size() < 1) {
        cout << "WARNING : this video doesn't contain enough captures for a "
          "camera calibration" << endl;
    }

    return NO_ERROR;
}
