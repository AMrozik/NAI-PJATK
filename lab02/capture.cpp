#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>

int main( int argc, char** argv ) {
    bool capturing = true;
    int width = 320;
    int height = 200;

    int H_max = 122;
    int H_min = 0;
    int S_max = 122;
    int S_min = 0;
    int V_max = 122;
    int V_min = 0;
    const int alpha_slider_max = 255;

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
        cv::Mat frame, frame_HSV, ss, inRange_frame;
        if (cap.read(frame)) {

            cv::resize(frame, frame, {width, height});
            // cv::flip(frame, frame , +1);

            cv::GaussianBlur(frame, frame, cv::Size(5,5), 0, 0);


            // Convert from BGR to HSV colorspace
            cv::cvtColor(frame, frame_HSV, cv::COLOR_BGR2HSV);

            cv::imshow( "almost smart window", frame );

            cv::createTrackbar( "H_Max_TrackBar", "In_Range", &H_max, alpha_slider_max);
            cv::createTrackbar( "H_Min_TrackBar", "In_Range", &H_min, alpha_slider_max);
            cv::createTrackbar( "S_Max_TrackBar", "In_Range", &S_max, alpha_slider_max);
            cv::createTrackbar( "S_Min_TrackBar", "In_Range", &S_min, alpha_slider_max);
            cv::createTrackbar( "V_Max_TrackBar", "In_Range", &V_max, alpha_slider_max);
            cv::createTrackbar( "V_Min_TrackBar", "In_Range", &V_min, alpha_slider_max);

            cv::inRange(frame_HSV, cv::Scalar(H_min, S_min, V_min), cv::Scalar(H_max, S_max, V_max), inRange_frame);

            cv::putText(frame_HSV, std::to_string(H_min) + "   " + std::to_string(H_max), {10, 30}, cv::FONT_HERSHEY_PLAIN, 1.0, {0,255,0,255});
            cv::putText(frame_HSV, std::to_string(S_min) + "   " + std::to_string(S_max), {10, 40}, cv::FONT_HERSHEY_PLAIN, 1.0, {0,255,0,255});
            cv::putText(frame_HSV, std::to_string(V_min) + "   " + std::to_string(V_max), {10, 50}, cv::FONT_HERSHEY_PLAIN, 1.0, {0,255,0,255});

            cv::imshow("HSV", frame_HSV);
            cv::imshow("In_Range", inRange_frame);
        } else {
            // stream finished
            capturing = false;
        }

        char k = cv::waitKey(5);
        if(k == 'x'){
          auto r = cv::selectROI("almost smart window", frame);
          ss = frame(r);
          cv::imshow("ScreenShot", ss);
          std::string ss_name;
          std::cout << "Podaj nazwę obrazka" << std::endl;
          std::cin >> ss_name;
          cv::imwrite(ss_name+".png", ss);
        }
        if(k == 27) capturing = false;
    } while( capturing );
    return 0;
}
