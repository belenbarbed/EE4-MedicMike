#!/usr/bin/env python
import rospy
## INCLUDE MESSAGE DIRECTORY EG from std_msgs.msg import String

class BaxterPackageDB:
    #def __init__(self):

    def listen_for_alerts(self):
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber("chatter", PackageAlert, callback)
        rospy.spin()

    def callback(self, data):
        CIDNumber = PackageInfoIn.CIDNumber
        Address = PackageInfoIn.Address
        Store = PackageInfoIn.Store



    def add_package_to_database(self):



    def retrieve_package_from_database(self):



    def publish_location_info(self):
