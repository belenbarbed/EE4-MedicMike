#!/usr/bin/env python

import sys
import ros
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import face_recognition
import pickle
import cv2
from ../MessageFiles/FR_message import IdentificationOut
from os import listdir

class FacialRecognition:


    def __init__(self):
        self.face_name_file = 'face_name.pkl'
        self.face_enc_file = 'face_enc.pkl'
        self.video_capture = cv2.VideoCapture(0)
        self.known_face_encodings = []
        self.known_face_names = []
        self.arrived = []
        self.pub = rospy.Publisher("DBChannel_In", IdentificationOut, queue_size=10)

    def pickup_listener(self):
        rospy.spin()

    def face_rec_learn(self):
        images = listdir("known_people")
        # print(images)
        for filename in images:
            self.known_face_names.append(filename.split('.')[0])
            filename = 'known_people/' + filename
            image_file = face_recognition.load_image_file(filename)
            enc_face = face_recognition.face_encodings(image_file)
            print(image_file.shape)
            self.known_face_encodings.append(enc_face[0])
        with open(self.face_name_file, "wb") as fp:
            pickle.dump(self.known_face_names, fp)
        with open(self.face_enc_file, "wb") as fp:
            pickle.dump(self.known_face_encodings, fp)

    

    # Create arrays of known face encodings and their names
    def recogniseFace(self):
        with open(self.face_name_file, "rb") as fp:
            self.known_face_names = pickle.load(fp)
        if len(self.known_face_names) != len(listdir("known_people")):
            face_rec_learn()
        else:
            with open(self.face_enc_file, "rb") as fp:
                self.known_face_encodings = pickle.load(fp)
    # Initialize some variables
        face_locations = []
        face_encodings = []
        process_this_frame = True
        prev_name = "Unknown"
        seen = 0
        not_seen = 0
        print_name = False
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
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                # face_names = []
                name = "Unknown"
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    # face_names.append(name)
            if name != "Unknown" and prev_name == name:
                seen += 1
            elif prev_name == "Unknown" and not_seen < 100:
                not_seen += 1
            else:
                seen = 0
            prev_name = name
            if seen >= 2 and name not in self.arrived:
                msg = IdentificationOut()
                msg.NHSNumber(uint32(name))
                print(name)
                self.arrived.append(name)
                rospy.loginfo(msg)
                self.pub.publish(msg)
                not_seen = 0
                print_name = True
            elif seen == 0:
                print_name = False
                
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
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video_capture.release()

        def hand

    # Release handle to the webcam
    # cv2.destroyAllWindows()
