printf "POST BOT PAT ROS WORKSPACE SETUP \n"
printf "============================================================= \n"

printf "This script will run all commands to create a ROS worksapce, ros_ws in your home directory \n"

read -n 1 -s -r -p "Press any key to continue"

printf "Running 1.2 of ROS getting started guide \n"
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

printf "Running 1.3 of ROS getting started guide \n"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
read -n 1 -s -r -p "If no errors, press any key to continue. If errors seek help! \n"

printf "updating apt-get \n"
sudo apt-get update

printf "installing ROS Kinetic \n"
sudo apt-get install ros-kinetic-desktop-full

sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list'
wget http://packages.ros.org/ros.key -O - | sudo apt-key add -
sudo apt-get install python-catkin-tools

read -n 1 -s -r -p "If no errors, press any key to continue. If errors seek help! \n"

printf "Inititalising rosdep  \n"
sudo rosdep init
printf "running rosdep update \n"
rosdep update

printf "Placing ros setup.bash in linux bash \n"
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

printf "Installing ROS package builders \n"
sudo apt-get install python-rosinstall python-rosinstall-generator python-wstool build-essential

printf "ROS install complete \n"
printf "Now will install baxter components \n"
printf "=========================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"

printf "creating ROS workspace \n"
mkdir -p ~/ros_ws/src

printf "will now attempt to run catkin_make \n"
read -n 1 -s -r -p "Press any key to continue"

cd ~/ros_ws
catkin_make
catkin_make install


printf "installing Baxter SDK Dependencies \n"
read -n 1 -s -r -p "Press any key to continue"

sudo apt-get update
sudo apt-get install git-core python-argparse python-wstool python-vcstools python-rosdep ros-kinetic-control-msgs ros-kinetic-joystick-drivers

printf "installing Baxter SDK\n"
read -n 1 -s -r -p "Press any key to continue \n"
cd ~/ros_ws/src
wstool init .
wstool merge https://raw.githubusercontent.com/RethinkRobotics/baxter/master/baxter_sdk.rosinstall
wstool update

printf "will now attempt to run catkin_make \n"
read -n 1 -s -r -p "Press any key to continue"

cd ~/ros_ws
catkin_make
catkin_make install

printf "Configuring Baxter Comms / ROS workspace\n"
printf "====================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"

printf "downloading baxter.sh script \n"
wget https://github.com/RethinkRobotics/baxter/raw/master/baxter.sh
chmod u+x baxter.sh

printf "Opening baxter.sh for editing. See setup instructions\n"
printf "====================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"

cd ~/ros_ws
gedit baxter.sh

printf "Please edit, save and close baxter.sh\n"
printf "====================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"
printf "\n If entry into the Baxter workspace is successfull type exit and press return \n"

cd ~/ros_ws
. baxter.sh

printf "Confirm entry into baxter workspace \n"
printf "====================================================== \n"
read -n 1 -s -r -p "Press any key to continue \n"

exit
