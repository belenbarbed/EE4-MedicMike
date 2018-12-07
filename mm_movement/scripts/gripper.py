#!/usr/bin/env python

'''
Script to open or close the hand grippers

run with:
rosrun mm_movement gripper.py -r/-l -o/-c
'''

import argparse

import rospy

import baxter_interface
import baxter_external_devices

from baxter_interface import CHECK_VERSION

from mm_movement.msg import EndEffectorState

gripper_force = 0
gripper_pos = 0

def gripper_data(data):
    gripper_force = data.force
    gripper_pos = data.position

def get_gripper(g):
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled    
    if(g == 'left'):
        return baxter_interface.Gripper('left', CHECK_VERSION)
    else:
        return baxter_interface.Gripper('right', CHECK_VERSION)

def init_gripper():
    left = get_gripper('left')
    left.calibrate
    right = get_gripper('right')
    right.calibrate

    
def offset_position(gripper, offset):
    if gripper.type() != 'electric':
        capability_warning(gripper, 'command_position')
        return
    current = gripper.position()
    #rospy.loginfo("Current Position: " + str(gripper.position()))
    #rospy.loginfo("Current Offset: " + str(offset))
    gripper.command_position(current + offset)
    #rospy.loginfo("Gripper Moved to Position: " + str(gripper.position()))
    
def gripper_action(action, arm):
    rospy.loginfo("Moving Gripper")
    count = 0
    if(action == 'open'):
        while count < 20:
            offset_position(get_gripper(arm), 15.0)
            count = count + 1
    elif(action == 'close'):
        while gripper_force < 10 and count < 20:
            offset_position(get_gripper(arm), -15.0)
            count = count + 1

def main():

    parser = argparse.ArgumentParser(description='Command for open/close the gripper')

    parser.add_argument('-l', default=False, action='store_true', dest='left',
        help='move the left gripper')
    parser.add_argument('-r', default=False, action='store_true', dest='right',
        help='move the right gripper')
        
    parser.add_argument('-c', default=False, action='store_true', dest='close',
        help='close gripper')
    parser.add_argument('-o', default=False, action='store_true', dest='open',
        help='open gripper')

    args = parser.parse_args()

    rospy.loginfo("Initializing node... ")
    rospy.init_node("gripper_action")
    rospy.loginfo("Initializing node... ")
    rospy.Subscriber("/robot/end_effector/left_gripper/state", EndEffectorState, gripper_data)

    arm = 'left'
    if (args.right):
        arm = 'right'
        
    action = 'open'
    if (args.close):
        action = 'close'

    gripper_action(action, arm)
         
    rospy.loginfo("Finished gripper_action")

if __name__ == "__main__":
    main()

