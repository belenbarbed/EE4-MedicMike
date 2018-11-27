#!/usr/bin/env python
import rospy
from baxter_common_msgs import EndEffectorState

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/robot/end_effector/left_gripper/state", EndEffectorState, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
