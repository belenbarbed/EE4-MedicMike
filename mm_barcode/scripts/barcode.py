#!/usr/bin/env python
import rospy
import time
import datetime
import numpy

from mm_barcode.msg import OCR_message
from mm_barcode.msg import Prescription_message

def main():
    pub = rospy.Publisher('OCR_DB_Channel', OCR_message, queue_size=10)
    rospy.init_node('barcode_reading', anonymous=True)
    rospy.loginfo("BARCODE SCANNING FOR MEDIC MIKE")
    while(1):
        rospy.loginfo("Waiting for code")
        text = raw_input()
        rospy.loginfo(text)
        data = text.split("/")
        nhsid = numpy.uint32(data[0])
        med = str(data[1])
        med = med.capitalize()
        
        msg = OCR_message()
        pre = Prescription_message()
        pre.MedicineName = med
        pre.RepeatPrescription = "N"
        pre.Dose = "2 pills"
        pre.TimesPerDay = numpy.uint8(1)
        pre.StartDate = rospy.Time()
        pre.Duration = numpy.uint8(10)
        msg.NHSNumber = nhsid
        msg.Prescription_Info = pre
        
        pub.publish(msg)

if __name__ == "__main__":
    main()

