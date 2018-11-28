#!/usr/bin/env python

'''
Script to pick medicine box from storage unit and chand it to the customer

run with:
rosrun mm_movement deliver_box.py -s <slot_number>
or
rosrun mm_movement deliver_box.py -s 0
to make it listen to the DB topic
'''

import argparse
import rospy
import time

from pick_place import EndPoint, makeQuaternion
from gripper import gripper_action
from mm_movement.msg import DB_output

from geometry_msgs.msg import (
    Quaternion,
)

# Orientations
vertical = makeQuaternion(0.00, 0.99, 0.03, 0.00) 
wayptor = makeQuaternion(-0.40, 0.91, 0.04, 0.07)         
horizontal = makeQuaternion(0.57, -0.56, -0.45, -0.40)

# Positions
handin = EndPoint(0.76, 0.14, 0.09, vertical)
waypoint = EndPoint(0.47, 0.72, 0.43, wayptor)
slots = [
    EndPoint(0.0, 0.0, 0.0, vertical),
    EndPoint(0.00, 1.12, 0.14, horizontal),
    EndPoint(0.11, 1.14, 0.14, horizontal),
    EndPoint(0.22, 1.15, 0.14, horizontal),
    EndPoint(0.31, 1.15, 0.13, horizontal)
]

def main():
    parser = argparse.ArgumentParser(description='Deliver medicine from storage slot')

    parser.add_argument('-s', type=int, dest='slot',
        help='the slot number, 1-4')
        
    args = parser.parse_args()

    rospy.loginfo("Initializing node... ")
    rospy.init_node("deliver_box")
    rospy.loginfo("Initializing node... ")

    if(args.slot == 0):
        # listen to topics instead
        rospy.Subscriber("DB_Move_Channel", DB_output, pass_slot)
        rospy.spin()
    else:
        # use command line args
        deliver_box(args.slot)

def pass_slot(data):
    if(data.Column == 0):
        # no prescription of user in sight
        return
    deliver_box(data.Column)

def deliver_box(slot):
    handin.goTo('left')
    gripper_action('open', 'left')
    waypoint.goTo('left')
    
    slots[slot].goTo('left')
    slots[slot].goToGrab('left')
    gripper_action('close', 'left')
    slots[slot].goToClear('left')
        
    waypoint.goTo('left')
    handin.goTo('left')
    time.sleep(2)
    gripper_action('open', 'left')

    # TODO: publish to topic confirming delivery of prescription to user
    
    rospy.loginfo("Finished deliver_box")

if __name__ == "__main__":
    main()
