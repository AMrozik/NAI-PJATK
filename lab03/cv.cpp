#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

using namespace cv;
using namespace std;


class MyObject {
public:
  int maxC;
  std::vector<Point> pos;
  Point getPosition(){
    if (pos.size() == 0) return Point(0,0);
    Point sum = std::accumulate(pos.begin(),pos.end(), Point(0,0));
    sum.x /= pos.size();
    sum.y /= pos.size();
    return sum;
  }

  void addPoint(Point p){
    pos.push_back(p);
    if(pos.size() > maxC){
      pos = vector<Point>(pos.begin()+1, pos.end());
    }
  }

  void addEmpty(){
    if(pos.size() > maxC){
      pos = vector<Point>(pos.begin()+1, pos.end());
    }
  }
};


int main() {
	int loRange[3] = {88,145,64};
	int hiRange[3] = {255,255,255};

	namedWindow("jakostam", cv::WINDOW_AUTOSIZE);
	createTrackbar("loRange0", "jakostam",&(loRange[0]), 255);
	createTrackbar("loRange1", "jakostam",&(loRange[1]), 255);
	createTrackbar("loRange2", "jakostam",&(loRange[2]), 255);
	createTrackbar("hiRange0", "jakostam",&(hiRange[0]), 255);
	createTrackbar("hiRange1", "jakostam",&(hiRange[1]), 255);
	createTrackbar("hiRange2", "jakostam",&(hiRange[2]), 255);
	VideoCapture camera(0);
	//VideoCapture backgroundvid("Multiwave.wmv");
	// Mat background = imread("plaza.jpg", cv::IMREAD_COLOR);

  MyObject myobj1, myobj2;
  myobj1.maxC = 10;
  myobj2.maxC = 10;
	while ( waitKey(1) != 27  ) {

    int dilation_size = 5;
    auto structElem = getStructuringElement( MORPH_ELLIPSE,
                                       Size( 2*dilation_size + 1, 2*dilation_size+1 ),
                                       Point( dilation_size, dilation_size ) );

		Mat frame;
		Mat backgroundScaled;
		Mat frameMask,frameNegMask;
		Mat frameWithMask,backgroundScaledWithMask;
		Mat meInNicePlace;

		camera >> frame;
		flip(frame, frame, 1);
    resize(frame, frame, {800, 600});
		// resize(background, backgroundScaled,{frame.cols, frame.rows});
		cvtColor(frame, frameMask, cv::COLOR_BGR2HSV);

		inRange(frameMask, Scalar(loRange[0],loRange[1],loRange[2]),
						Scalar(hiRange[0],hiRange[1],hiRange[2]), frameNegMask);


    morphologyEx(frameNegMask, frameNegMask, MORPH_CLOSE, structElem);
    morphologyEx(frameNegMask, frameNegMask, MORPH_OPEN, structElem);
    // imshow("dilate", frameNegMask);
    // imshow("orig", frame);

    std::vector<std::vector<Point>> contours;
    findContours(frameNegMask, contours, cv::RETR_LIST, cv::CHAIN_APPROX_TC89_KCOS);


    sort(contours.begin(), contours.end(),
              [](auto &a, auto &b){
                return contourArea(a, false) > contourArea(b,false);
              });

    // sort(contours.begin(), contours.end(),
		// 	 [](auto &a, auto &b) {
		// 		 return contourArea(a, false) > contourArea(b, false);
		// 	 });

    for(int i=0; i < contours.size(); i++){
        approxPolyDP(contours.at(i),contours.at(i),10,true);
        // drawContours(frame, contours, i, {0,0,255,255});
        // auto textpos = contours.at(i).at(0);
        // putText(frame, std::to_string(contours.at(i).size()), textpos, cv::FONT_HERSHEY_PLAIN,2,{0,0,255,255});
        // textpos.y += 30;
        // putText(frame, std::to_string(contourArea(contours.at(i), false)), textpos, cv::FONT_HERSHEY_PLAIN,2,{0,0,255,255});
        // textpos.y -= 60;
        // putText(frame, std::to_string(i), textpos, cv::FONT_HERSHEY_PLAIN,2,{0,0,255,255});
    }
    // imshow("contours", frame);

    if(contours.size()){
      Point avg;
      Rect r1 = boundingRect(contours.at(0));
      avg.x = r1.x+r1.width/2;
      avg.y = r1.y+r1.height/2;
      myobj1.addPoint(avg);
      // putText(frame, "0", avg, cv::FONT_HERSHEY_PLAIN,2,{0,255,255,255});
        if (contours.size() > 1){
            Rect r2 = cv::boundingRect(contours.at(1));
            avg.x = r2.x+r2.width/2;
            avg.y = r2.y+r2.height/2;
            myobj2.addPoint(avg);

            if(!(r1.y > r2.y + 45 || r2.y > r1.y + 45))
              cv::line(frame, myobj1.getPosition(), myobj2.getPosition(), cv::Scalar(0,0,0), 2);

      }
      else{
          myobj2.addEmpty();
      }
    } else {
        myobj1.addEmpty();
        myobj2.addEmpty();
    }
    // if (myobj1.pos.size() > 1){
    //     putText(frame, "X", myobj1.getPosition(), cv::FONT_HERSHEY_PLAIN,2,{0,255,255,255});
    //     putText(frame, "X", myobj2.getPosition(), cv::FONT_HERSHEY_PLAIN,2,{0,255,255,255});
    //
    //     // vector<vector<Point>>ctrs = {myobj1.pos};
    //     // drawContours(frame, ctrs, 0, {255,0,255,255});
    // }
    imshow("contours", frame);
	}
	return 0;
}
