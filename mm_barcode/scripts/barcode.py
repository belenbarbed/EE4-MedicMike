#!/usr/bin/env python

import rospy
import time
from mm_barcode.msg import OCR_message

def main():
    pub = rospy.Publisher('OCR_DB_Channel', OCR_message, queue_size=10)
    rospy.init_node('barcode_reading', anonymous=True)
    rospy.loginfo("BARCODE SCANNING FOR MEDIC MIKE")
    while(1):
        rospy.loginfo("Waiting for code")
        text = raw_input()
        rospy.loginfo(text)
        data = text.split("/")
        nhsid = str(data[0])
        med = str(data[1])
        med = med.capitalize()
        msg = OCR_message()
        msg.NHSNumber = nhsid
        msg.Prescription_Info = med
        pub.publish(msg)

if __name__ == "__main__":
    main()

