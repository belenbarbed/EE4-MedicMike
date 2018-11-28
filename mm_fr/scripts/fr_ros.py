#!/usr/bin/env python

import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import face_recognition
import rospy
import pickle
import cv2
import os
import time
import numpy as np
from mm_fr.msg import DB_output
from mm_fr.msg import FR_message
from mm_fr.msg import Collect_message
from os import listdir


class FacialRecognition:

    def __init__(self):
        self.file_loc = os.path.dirname(__file__)
        self.face_name_file = self.file_loc + '/face_name'
        self.face_enc_file = self.file_loc + '/face_enc'
        self.video_capture = cv2.VideoCapture(0)
        self.known_face_encodings = []
        self.known_face_names = []
        self.arrived = []
        self.unknownHandled = True
        rospy.init_node('FacialRecognition', anonymous=True)
        rospy.Subscriber("Collected_Channel", Collect_message,
                         self.__Collectcallback)
        rospy.Subscriber("DB_Move_Channel", DB_output, self.__DBcallback)
        self.pub = rospy.Publisher("FR_DB_Channel", FR_message, queue_size=10)

    def pickup_listener(self):
        rospy.spin()

    def __DBcallback(self, data):
        row = data.Row
        col = data.Column
        patient_NHS_number = str(data.NHSNumber)
        # if row == 0 and col == 0 and patient_NHS_number != "0":
        #     self.arrived.remove(patient_NHS_number)

    def __Collectcallback(self, data):
        patient_NHS_number = str(data.NHSNumber)
        if patient_NHS_number == "0":
            self.unknownHandled = False
        else:
            self.arrived.remove(patient_NHS_number)
        time.sleep(5)

    def face_rec_learn(self):
        images = listdir("known_people")
        # print(images)
        for filename in images:
            self.known_face_names.append(filename.split('.')[0])
            filename = self.file_loc + '/known_people/' + filename
            image_file = face_recognition.load_image_file(filename)
            enc_face = face_recognition.face_encodings(image_file)
            print(image_file.shape)
            self.known_face_encodings.append(enc_face[0])
        np.save(self.face_name_file, self.known_face_names)
        np.save(self.face_enc_file, self.known_face_encodings)

    # Create arrays of known face encodings and their names
    def recogniseFace(self):
        self.known_face_names = np.load(self.face_name_file+'.npy').tolist()
        if len(self.known_face_names) != len(listdir(self.file_loc + "/known_people")):
            self.face_rec_learn()
        else:
            self.known_face_encodings = np.load(
                self.face_enc_file+'.npy').tolist()
    # Initialize some variables
        face_locations = []
        face_encodings = []
        process_this_frame = True
        prev_name = "0"
        seen = 0
        not_seen = 0
        unknown = False
        while True:
            # Grab a single frame of video
            ret, frame = self.video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(
                    rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)

                # face_names = []
                for face_encoding in face_encodings:
                    name = "0"
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, face_encoding)

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.known_face_names[first_match_index]

                    # face_names.append(name)
                    if prev_name == name and name == "0":
                        not_seen += 1
                    elif prev_name == name:
                        seen += 1
                        unknown = False
                    if not_seen > 3:
                        unknown = True
                        seen = 0
                    prev_name = name
                    if (seen >= 2 or unknown == True) and self.arrived == []:
                        unknown == False
                        FR_msg = FR_message()
                        FR_msg.NHSNumber = long(name)
                        self.arrived.append(name)
                        rospy.loginfo(name + ' recognised')
                        self.pub.publish(FR_msg)
                        not_seen = 0
                    # elif seen == 0 and "0" not in self.arrived and unknown == True:
                    #     FR_msg = FR_message()
                    #     FR_msg.NHSNumber = long(name)
                    #     self.arrived.append(name)
                    #     rospy.loginfo('Unknown face recognised')
                    #     self.pub.publish(FR_msg)

            process_this_frame = not process_this_frame

            # Display the results
            # for (top, right, bottom, left), name in zip(face_locations, face_names):
            #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #     top *= 4
            #     right *= 4
            #     bottom *= 4
            #     left *= 4

            #     # Draw a box around the face
            #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)

            #     # Draw a label with a name below the face
            #     cv2.rectangle(frame, (left, bottom ), (right, bottom + 35), (0, 0, 255), cv2.FILLED)
            #     font = cv2.FONT_HERSHEY_DUPLEX
            #     cv2.putText(frame, name, (left + 6, bottom + 30), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image

            # Hit 'q' on the keyboard to quit!
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        self.video_capture.release()


FaceRec = FacialRecognition()
FaceRec.recogniseFace()
# Release handle to the webcam
# cv2.destroyAllWindows()
