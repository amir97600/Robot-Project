#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <string>

using namespace cv;

const char* about =
        "Display an image.\n"
        "  Program to display an image.\n";
const char* keys  =
        "{h       |       | Display help }"
        "{@infile |<none> | Image to display }";

int main(int argc, char** argv )
{

    CommandLineParser parser(argc, argv, keys);
    parser.about(about);

    if((argc != 2) || parser.has("h") || parser.has("help")){
        parser.printMessage();
        return -1;
    }

    String image_path = parser.get<String>(0);

    Mat image;
    image = imread( image_path, 1 );
    if ( !image.data )
    {
        printf("This is not an image data. \n");
        return -1;
    }
    namedWindow("Display Image", WINDOW_AUTOSIZE );
    imshow("Display Image", image);
    waitKey(0);
    return 0;
}
