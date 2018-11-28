#!/usr/bin/env python
import rospy

import spacy  # speech processing API
import pyaudio # importing audio from microphone
import speech_recognition as sr # Speech-To-Text library
import pyttsx # Text-To-Speech 

from mm_spr.msg import FR_message  

engine = pyttsx.init()
nlp = spacy.load('en_core_web_sm')


def listen():
	r = sr.Recognizer()
	sr.Microphone()
	with sr.Microphone() as source:
	    r.adjust_for_ambient_noise(source)
	    print("Listening...")
	    audio = r.listen(source, timeout=8)

	print("Got it, you said...")
	text = r.recognize_google(audio)
	print(text)

def check_answer(answer):
        if (token.text == 'yes') or (token.text == 'Yes'):
            answer=True
            return answer
        else:
            answer=False
            return answer

def scan_prescription():
    engine.say('Please place it within the frame, so I can scan the document')
    # publish scanning to OCR
    SPR_msg = SPR_message()
    SPR_msg.Scan = "START_OCR"
    pub = rospy.Publisher("SPR_OCR_Channel", SPR_message, queue_size=10)
    pub.publish(SPR_msg)

def interact(data):
    if data.NHSNumber == 0:   # person unrecognised
        engine.say('Dont recognise you, do you have a paper prescription?')
	audio = listen()
	#expected_audio=nlp(u"yes")	
	paper_prescription=check_answer(audio)
	if paper_prescription:
	   scan_prescription()
	#else
	   # publish--useless person

    else:  #person recognised
        engine.say('Hello, hold on a second while we retrieve your medicines')
	# ignore now--check if its in stock or not
	# ignore now--if they have any medicines or not	


def main():
	rospy.init_node('greeting', anonymous=True)
	rospy.Subscriber("FR_DB_Channel", FR_message, interact) 
	# subscribe to movement 
	rospy.spin()

if __name__ = '__main__':
	main()
