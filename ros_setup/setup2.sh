printf "Part 2 of ROS Baxter setup \n"


printf "Will now install Baxter simulator"
printf "====================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"

sudo apt-get install gazebo7 ros-kinetic-qt-build ros-kinetic-gazebo-ros-control ros-kinetic-gazebo-ros-pkgs ros-kinetic-ros-control ros-kinetic-control-toolbox ros-kinetic-realtime-tools ros-kinetic-ros-controllers ros-kinetic-xacro python-wstool ros-kinetic-tf-conversions ros-kinetic-kdl-parser

cd ~/ros_ws/src
wstool init .
wstool merge https://raw.githubusercontent.com/RethinkRobotics/baxter_simulator/kinetic-devel/baxter_simulator.rosinstall
wstool update


printf "Now attempting catkin_make \n"
read -n 1 -s -r -p "Press any key to continue \n"

cd ~/ros_ws
catkin_make
cp src/baxter/baxter.sh .


printf "Opening baxter.sh for editing. See setup instructions\n"
printf "====================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"

cd ~/ros_ws
gedit baxter.sh

printf "Please edit, save and close baxter.sh\n"
printf "====================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"

printf "cloning Post Bot Pat Repo into /src \n"
printf "====================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"

cd ~/ros_ws/src
git init
git add remote origin https://github.com/belenbarbed/EE4-PostBotPat
git add .
git commit -m "commit from setup bash 2"
git pull origin master

printf "attempting catkin_make, if no errors then setup complete \n"
printf "====================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"

catkin_make
