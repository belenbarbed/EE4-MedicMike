# EE4-MedicMike
HCR Coursework 2018

Medic Mike is an implementation on the robot Baxter that enables it to operate as a pahrmaceutical assistant, recognising customers and medical prescription to hand you the medicine you need in an automated manner.

## Directory Structure

```
~/ros_ws
    baxter.sh
    build/
    devel/
    src/                 => GIT REPO - what we handed in
        .gitignore
        README.md
        mm_movement/
            scripts/
                deliver_box.py
                ...
        mm_spr/
            scripts/
                speech.py
        ...
```

## How to install

1. Run our setup.sh script (in the folder ros_setup) to set up the Baxter workspace:
```
chmod +x ./setup.sh
./setup.sh
```
In the 2 cases when vim opens, change the following lines:
```
baxter_hostname="something.local"
```
to
```
baxter_hostname="011401P0008.local"
```
and
```
your_ip="192.168.XXX.XXX"
```
to have your computer's IP address

and
```
ros_version="indigo"
```
to
```
ros_version="kinetic"
```

2. Run our setup2.sh script to set up the repo within the src of the catkin workspace:
```
chmod +x ./setup2.sh
./setup2.sh
```

## Running the Baxter simulator

In 2 terminal tabs, run:
```
cd ~/ros_ws
./baxter.sh sim
```
In the 1st tab, run:
```
roslaunch baxter_gazebo baxter_world.launch
```
The gazebo terminal window should open with the robot in the world.

Then, in the 2nd terminal tab:
```
rosrun baxter_tools enable_robot.py -e
```
You can now run python scripts in the 2nd terminal to move Baxter and see it in the gazebo simulator. For example:
```
rosrun mm_movement deliver_box.py -s 3
```
