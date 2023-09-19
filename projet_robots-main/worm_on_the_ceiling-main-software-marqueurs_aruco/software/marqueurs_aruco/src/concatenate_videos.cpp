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

typedef enum {
  NO_ERROR = 0,
  NOT_ENOUGH_CAPTURES = 1,
  NOT_ENOUGHT_CORNERS = 2,
  FAIL_TO_SAVE_OUTPUT_FILE = 3,
  INVALID_NUMBER_OF_PARAMETERS = 4,
  PARAMETERS_FILE_CANT_BE_READEN = 5,
  PARAMETERS_ARE_NOT_VALID = 6
} Error_code;

typedef struct {
  vector<string> input_videos;
  VideoCapture video_capture;

  string outputFile;
} Video_data;

int parse_command_line(
  Video_data & video_data, int argc, char *argv[]
){
  if(argc < 3) {
    std::cout << "Usage : " << argv[0] << " input_video_1 [input_video_2 ...] output_video"  << std::endl;
    return INVALID_NUMBER_OF_PARAMETERS;
  }
    
  for(int i = 1; i < argc-1; i++){
    video_data.input_videos.push_back( std::string(argv[i]) );
  }

  video_data.outputFile = std::string( argv[argc-1] );
  
  return NO_ERROR;
}

int main(int argc, char *argv[]) {
    int error_code = NO_ERROR;
    Video_data video_data;

    error_code = parse_command_line(video_data, argc, argv);
    if( error_code ) return error_code;

    vector< Mat > allImgs;
    Size imgSize;
    for( unsigned int i=0; i < video_data.input_videos.size(); i++ ){
      video_data.video_capture.open(video_data.input_videos[i]);
      while(video_data.video_capture.grab()) {
        Mat image, imageCopy;
        video_data.video_capture.retrieve(image);

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

    return NO_ERROR;
}
