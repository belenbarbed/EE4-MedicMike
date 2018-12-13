cmake_minimum_required(VERSION 2.8.3)
project(mm_ocr)



## Compile as C++11, supported in ROS Kinetic and newer
## `pkg-config --cflags --libs lept tesseract opencv`
add_compile_options(-std=c++11 -ggdb -llept -ltesseract -lopencv_core -lopencv_highgui -lopencv_dnn -lopencv_text -lopencv_bridge)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  message_generation
)

## System dependencies are found with CMake's conventions
find_package(OpenCV 4 REQUIRED 
	core imgproc highgui dnn text
	PATHS /usr/local 
	NO_DEFAULT_PATH
)

add_message_files(
   FILES
   OCR_message.msg
   SPR_message.msg
 )

 generate_messages(
   DEPENDENCIES
   std_msgs
 )

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
   INCLUDE_DIRS include
   LIBRARIES mm_ocr TESSERACT
   CATKIN_DEPENDS roscpp std_msgs message_runtime
   DEPENDS cv_bridge opencv dnn tesseract leptonica
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
 include
 ~/opencv/cmake/
  /usr/local/include/opencv4
  ${catkin_INCLUDE_DIRS}
)

## Declare a C++ libraryo
# add_library(${PROJECT_NAME}
#   src/${PROJECT_NAME}/rospipe.cpp
# )

#include_directories(${OpenCV_INCLUDE_DIRS})
## Declare a C++ executable
## With catkin_make all packages are built within a single CMake context
## The recommended prefix ensures that target names across packages don't collide
add_executable(mm_ocr src/rospipe.cpp)

## Add cmake target dependencies of the library
## as an example, code may need to be generated before libraries
## either from message generation or dynamic reconfigure
add_dependencies(mm_ocr ${mm_ocr_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

add_dependencies(mm_ocr roscpp_gencpp std_msgs_gencpp mm_ocr_gencfg mm_ocr_generate_messages_cpp)

## Specify libraries to link a library or executable target against
target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})
target_link_libraries(${PROJECT_NAME} lept tesseract /usr/local/lib)



