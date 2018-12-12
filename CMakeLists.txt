cmake_minimum_required(VERSION 2.8.3)
project(ocr_package)

## Compile as C++11, supported in ROS Kinetic and newer
## `pkg-config --cflags --libs lept tesseract opencv`
add_compile_options(-std=c++11 -ggdb -llept -ltesseract)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  message_generation
)

## System dependencies are found with CMake's conventions
find_package(OpenCV REQUIRED 
	NO_MODULE
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
   LIBRARIES ocr_package
   CATKIN_DEPENDS roscpp std_msgs message_runtime
   DEPENDS opencv tesseract leptonica
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
 include
  ${OpenCV_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
)

## Declare a C++ libraryo
# add_library(${PROJECT_NAME}
#   src/${PROJECT_NAME}/rospipe.cpp
# )


## Declare a C++ executable
## With catkin_make all packages are built within a single CMake context
## The recommended prefix ensures that target names across packages don't collide
add_executable(ocr_package src/rospipe.cpp)

## Add cmake target dependencies of the library
## as an example, code may need to be generated before libraries
## either from message generation or dynamic reconfigure
add_dependencies(ocr_package ${ocr_package_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

add_dependencies(ocr_package roscpp_gencpp std_msgs_gencpp ocr_package_gencfg ocr_package_generate_messages_cpp)


## Specify libraries to link a library or executable target against
target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})
target_link_libraries(${PROJECT_NAME} lept tesseract)



