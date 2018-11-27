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

gripper_force = 0

def force_check(data):
    gripper_force = data.force

def get_gripper(g):
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled
    left = baxter_interface.Gripper('left', CHECK_VERSION)
    right = baxter_interface.Gripper('right', CHECK_VERSION)
    
    if(g == 'left'):
        return left
    else:
        return right

    
def offset_position(gripper, offset):
    if gripper.type() != 'electric':
        capability_warning(gripper, 'command_position')
        return
    current = gripper.position()
    gripper.command_position(current + offset)
    
def gripper_action(action, arm):
    count = 0
    if(action == 'open'):
        while gripper_force > 0 and count < 20:
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
    rospy.Subscriber("/robot/end_effector/left_gripper/state", EndEffectorState, force_check)

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

