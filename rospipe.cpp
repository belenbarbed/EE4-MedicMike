#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/dnn.hpp>
#include <opencv2/opencv.hpp>
#include "opencv2/core/utility.hpp"
#include "opencv2/text.hpp"

#include <tesseract/baseapi.h>
#include <tesseract/ocrclass.h>
#include <leptonica/allheaders.h>

#include "ros/ros.h"
#include "std_msgs/String.h"

#include <iostream>
#include <sstream> // To build the message string in ros
#include <regex>
#include 

using namespace cv;
using namespace cv::dnn;
using namespace cv::text;

constexpr int INPWIDTH = 320;
constexpr int INPHEIGHT = 320;
constexpr float CONFTHRESHOLD = 0.5f;
constexpr float NMSTHRESHOLD = 0.4f;

constexpr uint32_t MAX_FRAMES = 100;

constexpr std::string OCR_NO_FRAME_ERROR = "OCR_NO_CAMERA_INPUT_ERROR";
constexpr std::string OCR_NO_MATCH_ERROR = "OCR_NO_MATCHED_STRING" 

// Global to be access across callbacks
VideoCapture vidcap;
ros::NodeHandle nodeHandler;

// Function prototypes
std::string performOcr();
void confirmStartOcrCallback(const std_msgs::String::ConstPtr& msg);
void decode(const Mat& scores, const Mat& geometry, float scoreThresh,
            std::vector<RotatedRect>& detections, std::vector<float>& confidences);

int main(int argc, char **argv)
{

    // Start the camera to reduce latency
    vidcap.open(0); // Check in Baxter which camera is being used

    // Initialize ROS and perform argument remapping (if required)
    ros::init(argc, argv, "ocr");

    // Start the subscriber to wait for the callback from the speech recognizer
    ros::Subscriber sub_OcrWait = nodeHandler.subscribe("SPR_OCR_Channel", 100, performOcrCallback(capture));

    return 0;
}

void confirmStartOcrCallback(const std_msgs::String::ConstPtr& msg)
{

    std::string ocr_ResultString;
    std::stringstream ss;
    std_msgs:: String rosmsg;

    // Check the subscribed topic string, if confirmation exists then enter the OCR routine
    std::string checkString = static_cast<std::string>(msg->data.c_str());

    // Start a publisher
    ros::Publisher pub_OcrExecute = nodeHandler.advertise<std_msgs::String>("OCR_DB_Channel", 100);
    ros::Rate loop_rate(10);

    if(checkString == "START_OCR")
    {
        ocr_ResultString = performOcr();
        // Publish the result string
        ss << ocr_ResultString;
        rosmsg.data = ss.str();
        // Check if the ROS system is ok to publish
        if(ros::ok())
        {
            pub_OcrExecute.publish(rosmsg);
            ros::spinOnce();
        }

    }
    else
    {

    }

}

std::string performOcr()
{
    String model = static_cast<String>("frozen_east_text_detection.pb");
    Net net;

    // Check if the model exists
    CV_Assert(!model.empty());

    // Load the network
    net = readNet(model);

    // The camera is already open, can just pass the capture to the frame

    static const std::string kWinName = "All Rectangles";
    namedWindow(kWinName, WINDOW_NORMAL);

    std::vector<Mat> outs;
    std::vector<String> outNames(2);
    outNames[0] = "feature_fusion/Conv_7/Sigmoid";
    outNames[1] = "feature_fusion/concat_3";

    Mat frame, blob, temp;

    for(int framecount = 0; framecount < MAXFRAMES; ++framecount)
    {
        vidcap >> frame;
        if (frame.empty())
        {
            // Publish an empty message
            return OCR_NO_FRAME_ERROR;
        }

        blobFromImage(frame, blob, 1.0, Size(INPWIDTH, INPHEIGHT), Scalar(123.68, 116.78, 103.94), true, false);
        net.setInput(blob);
        net.forward(outs, outNames);

        Mat scores = outs[0];
        Mat geometry = outs[1];

        // Decode predicted bounding boxes.
        std::vector<RotatedRect> boxes;
        std::vector<float> confidences;
        decode(scores, geometry, CONFTHRESHOLD, boxes, confidences);

        // Apply non-maximum suppression procedure
        std::vector<int> indices;
        NMSBoxes(boxes, confidences, CONFTHRESHOLD, NMSTHRESHOLD, indices);

        // Detections are rendered here but need the individual rectangles

        // Crop the image rectangles and process them individually, storing them in a vector
        Mat rotationMatrix, rotatedImage, initialCroppedImage, finalCroppedImage;
        float angle;
        Size box_size;
        std::vector<std::string> resultStrings;

        Point2f ratio((float)frame.cols / INPWIDTH, (float)frame.rows / INPHEIGHT);

        //bitwise_not(frame, frame);
        Ptr<OCRTesseract> ocr = OCRTesseract::create();

        for(size_t i = 0; i < indices.size(); ++i)
        {
            // Convert the rotated rectangle to a regular rectangle for Tesseract
            RotatedRect& box = boxes[indices[i]];

            box_size = box.size; // Iterating over the correct thing?
            std::cout << "Box Size pre ratio " << box_size << std::endl;

            // Get the rotation matrix
            rotationMatrix = getRotationMatrix2D(box.center, angle, 1.0);

            // Perform the rotation
            warpAffine(frame, rotatedImage, rotationMatrix, frame.size(), INTER_CUBIC);

            Point2f vertices[4];
            box.points(vertices);
            std::vector<Point> new_pts;

            for (int j = 0; j < 4; ++j)
            {
                vertices[j].x *= ratio.x;
                vertices[j].y *= ratio.y;
                new_pts.push_back(vertices[j]);
            }

            // Increase the size of the box
            RotatedRect all_box = minAreaRect(new_pts);

            // Crop the box from the image
            box_size = all_box.size;
            if(box.angle < -45.)
            {
                swap(box_size.width, box_size.height);
            }

            std::cout << "Box Size post ratio " << box_size << std::endl; 

            getRectSubPix(rotatedImage, box_size, all_box.center, initialCroppedImage);

            //imshow("cropped", initialCroppedImage);

            // save the image output here possibly to debug
            //imwrite(format("images/crops/crops_%04d.jpg", i), initialCroppedImage);

            for (int j = 0; j < 4; ++j)
            {
                line(frame, vertices[j], vertices[(j + 1) % 4], Scalar(0, 255, 0), 2);
            }

            // Pass the cropped rectangle to Tesseract
            // run(image, outputstring, &boxes, &words, &confidences, OCR_LEVEL_WORD)
            std::vector<Rect> boxes;
            std::vector<std::string> words;
            std::vector<float> confidences;
            std::string output; 
            ocr->run(initialCroppedImage, output, &boxes, &words, &confidences, OCR_LEVEL_WORD);

            //std::cout << "Tesseract Output: " << output << std::endl;
            resultStrings.push_back(output);
        }
    }


    // Regex for determining if the required string exists
    std::regex num_regex("[0-9]{9}");

    std::string compString;
    std::string foundString = OCR_NO_MATCH_ERROR;
    // Iterate through the results vector to see if any of the elements match the regex
    for(std::vector<std::string>::iterator it = resultStrings.begin(); it != resultStrings.end(); ++it)
    {
        compString = *it;
        if(std::regex_match(num_regex, compString)){
            foundString = compString;
            // Probably not best practice but oh well
            return foundString;
        }
    }

    return foundString;

}





void decode(const Mat& scores, const Mat& geometry, float scoreThresh,
            std::vector<RotatedRect>& detections, std::vector<float>& confidences)
{
    detections.clear();
    CV_Assert(scores.dims == 4); CV_Assert(geometry.dims == 4); CV_Assert(scores.size[0] == 1);
    CV_Assert(geometry.size[0] == 1); CV_Assert(scores.size[1] == 1); CV_Assert(geometry.size[1] == 5);
    CV_Assert(scores.size[2] == geometry.size[2]); CV_Assert(scores.size[3] == geometry.size[3]);

    const int height = scores.size[2];
    const int width = scores.size[3];
    for (int y = 0; y < height; ++y)
    {
        const float* scoresData = scores.ptr<float>(0, 0, y);
        const float* x0_data = geometry.ptr<float>(0, 0, y);
        const float* x1_data = geometry.ptr<float>(0, 1, y);
        const float* x2_data = geometry.ptr<float>(0, 2, y);
        const float* x3_data = geometry.ptr<float>(0, 3, y);
        const float* anglesData = geometry.ptr<float>(0, 4, y);
        for (int x = 0; x < width; ++x)
        {
            float score = scoresData[x];
            if (score < scoreThresh)
                continue;

            // Decode a prediction.
            // Multiple by 4 because feature maps are 4 time less than input image.
            float offsetX = x * 4.0f, offsetY = y * 4.0f;
            float angle = anglesData[x];
            float cosA = std::cos(angle);
            float sinA = std::sin(angle);
            float h = x0_data[x] + x2_data[x];
            float w = x1_data[x] + x3_data[x];

            Point2f offset(offsetX + cosA * x1_data[x] + sinA * x2_data[x],
                           offsetY - sinA * x1_data[x] + cosA * x2_data[x]);
            Point2f p1 = Point2f(-sinA * h, -cosA * h) + offset;
            Point2f p3 = Point2f(-cosA * w, sinA * w) + offset;
            RotatedRect r(0.5f * (p1 + p3), Size2f(w, h), -angle * 180.0f / (float)CV_PI);
            detections.push_back(r);
            confidences.push_back(score);
        }
    }
}