#!/usr/bin/env python
import rospy
from mm_movement.msg import EndEffectorState

def callback(data):
    rospy.loginfo(data.force + 3)
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/robot/end_effector/left_gripper/state", EndEffectorState, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
