#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
int main( int argc, char** argv ) {
    bool capturing = true;
    int width = 320;
    int height = 200;
    // Question for you
    // cv::VideoCapture cap( "szukaj_zielonego.webm" );
    cv::VideoCapture cap(0);
    if ( !cap.isOpened() ) {
        std::cerr << "error opening frames source" << std::endl;
        return -1;
    }

    if(argc >= 3){
      width = atoi(argv[1]);
      height = atoi(argv[2]);
    }
    printf("stream size: %dx%d\n", width, height);
    do {
        cv::Mat frame, frame_HSV;
        if (cap.read(frame)) {

            cv::resize(frame, frame, {width, height});
            // cv::flip(frame, frame , +1);

            cv::GaussianBlur(frame, frame, cv::Size(5,5), 0, 0);


            // Convert from BGR to HSV colorspace
            cvtColor(frame, frame_HSV, cv::COLOR_BGR2HSV);

            // show image frame by frame
            cv::imshow( "almost smart window", frame );
            cv::imshow("HSV", frame_HSV);
        } else {
            // stream finished
            capturing = false;
        }

        char k = cv::waitKey(5);
        if(k == 'x'){
          auto r = cv::selectROI("almost smart window", frame);
          cv::Mat ss = frame(r);
          cv::imshow("ScreenShot", ss);
        }
        if(k == 27) capturing = false;
    } while( capturing );
    return 0;
}
