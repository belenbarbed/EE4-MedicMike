import argparse

import rospy

import baxter_interface

def callback(msg):
    print (msg)

def main():
    rospy.init_node('listener')
    rospy.Subscriber('/robot/end_effector/left_gripper/state', 'baxter_core_msgs-EndEffectorState', callback)
    rospy.spin()
