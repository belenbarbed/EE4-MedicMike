#!/usr/bin/env python

'''
Script to pick medicine box from storage unit and chand it to the customer

run with:
rosrun mm_movement deliver_box.py -s <slot_number>
'''

import argparse
import rospy
import time

from pick_place import arm_move_to_pos
from gripper import gripper_action
from mm_movement.msg import DB_output

from geometry_msgs.msg import (
    Quaternion,
)

def main():
    parser = argparse.ArgumentParser(description='Deliver medicine from storage slot')

    parser.add_argument('-s', type=int, dest='slot',
        help='the slot number, 1-4')
        
    args = parser.parse_args()

    rospy.loginfo("Initializing node... ")
    rospy.init_node("deliver_box_test")
    rospy.loginfo("Initializing node... ")

    if(args.slot == 0):
        # listen to topics instead
        rospy.Subscriber("DB_Move_Channel", DB_output, pass_slot)
        rospy.spin()
    else:
        # use command line args
        deliver_box(args.slot)


def pass_slot(data):
    deliver_box(data.Column)

def deliver_box(slot):
    vertical = Quaternion(
                    x=0.00,
                    y=0.99,
                    z=0.03,
                    w=0.00,
                )
                
    waypoint = Quaternion(
                    x=-0.40,
                    y=0.91,
                    z=0.04,
                    w=0.07,
                )
                
    horizontal = Quaternion(
                    x=0.57,
                    y=-0.56,
                    z=-0.45,
                    w=-0.40,
                )

    arm_move_to_pos(0.76, 0.14, 0.09, 'left', vertical)
    gripper_action('open', 'left')
    arm_move_to_pos(0.47, 0.72, 0.43, 'left', waypoint)
    
    if(slot == 1):
        arm_move_to_pos(0.00, 1.12, 0.14, 'left', horizontal)
        arm_move_to_pos(0.00, 1.17, 0.14, 'left', horizontal)
        gripper_action('close', 'left')
        arm_move_to_pos(0.00, 1.02, 0.14, 'left', horizontal)
    elif(slot == 2):
        arm_move_to_pos(0.11, 1.14, 0.14, 'left', horizontal)
        arm_move_to_pos(0.11, 1.19, 0.14, 'left', horizontal)
        gripper_action('close', 'left')
        arm_move_to_pos(0.11, 1.04, 0.14, 'left', horizontal)
    elif(slot == 3):
        arm_move_to_pos(0.22, 1.15, 0.14, 'left', horizontal)
        arm_move_to_pos(0.22, 1.20, 0.14, 'left', horizontal)
        gripper_action('close', 'left')
        arm_move_to_pos(0.22, 1.04, 0.14, 'left', horizontal)
    elif(slot == 4):
        arm_move_to_pos(0.31, 1.15, 0.13, 'left', horizontal)
        arm_move_to_pos(0.31, 1.20, 0.13, 'left', horizontal)
        gripper_action('close', 'left')
        arm_move_to_pos(0.31, 1.05, 0.13, 'left', horizontal)
        
    arm_move_to_pos(0.47, 0.72, 0.43, 'left', waypoint)
    arm_move_to_pos(0.76, 0.14, 0.09, 'left', vertical)
    time.sleep(2)
    gripper_action('open', 'left')
    
    rospy.loginfo("Finished gripper_action")

if __name__ == "__main__":
    main()
