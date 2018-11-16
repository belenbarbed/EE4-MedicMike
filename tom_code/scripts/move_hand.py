"""
Baxter RSDK Inverse Kinematics Example
"""
import argparse
import struct
import sys

import rospy

import baxter_interface
import baxter_external_devices
import tf

from baxter_interface import CHECK_VERSION

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

def get_ik(pose, limb):
    ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
    iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
    ikreq = SolvePositionIKRequest()
    hdr = Header(stamp=rospy.Time.now(), frame_id='base')
    ikreq.pose_stamp.append(pose)
    try:
        rospy.wait_for_service(ns, 5.0)
        resp = iksvc(ikreq)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Service call failed: %s" % (e,))
        return None
    resp_seeds = struct.unpack('<%dB' % len(resp.result_type),
                               resp.result_type)
    if (resp_seeds[0] != resp.RESULT_INVALID):
        seed_str = {
                    ikreq.SEED_USER: 'User Provided Seed',
                    ikreq.SEED_CURRENT: 'Current Joint Angles',
                    ikreq.SEED_NS_MAP: 'Nullspace Setpoints',
                   }.get(resp_seeds[0], 'None')
        print("SUCCESS - Valid Joint Solution Found from Seed Type: %s" %
              (seed_str,))
        # Format solution into Limb API-compatible dictionary
        limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
        return limb_joints
    else:
        print("INVALID POSE - No Valid Joint Solution Found.")
        return None

def move_to_pos(xin,yin,zin):
    hdr = Header(stamp=rospy.Time.now(), frame_id='base')
    quater = Quaternion(
                    x=0.707,
                    y=0.0,
                    z=0.707,
                    w=0.0,
                )

    base_pose = PoseStamped(
            header=hdr,
            pose=Pose(
                position=Point(
                    x=xin,#0.8,
                    y=yin,#-0.95,
                    z=zin,#.6,
                ),
                orientation=quater
            ),
        )
    base_pos = get_ik(base_pose, 'right')
    arm = baxter_interface.Limb('right')
    arm.move_to_joint_positions(base_pos)
    print "move complete"

def main():
    rospy.loginfo("Initializing node... ")
    move_to_pos(0.8, -0.95, 0.6)
    rospy.loginfo("Finished move_hand")

if __name__ == "__main__":
    main()
