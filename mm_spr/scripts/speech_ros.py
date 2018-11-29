#!/usr/bin/env python
import rospy

import spacy  # speech processing API
import pyaudio # importing audio from microphone
import speech_recognition as sr # Speech-To-Text library
# import pyttsx
from gtts import gTTS
from mm_spr.msg import FR_message  
from mm_spr.msg import SPR_message  
from mm_spr.msg import Face_message  
import os

nlp = spacy.load('en_core_web_sm')

def talk(phrase):
	# engine = pyttsx.init()

	# engine.setProperty('voice', 'scottish')
	# engine.say(phrase)
	# engine.runAndWait()
	tts = gTTS(text=phrase, lang='en')
	tts.save("speech.mp3")
	os.system("mpg321 speech.mp3")

def listen():
    r=sr.Recognizer()
    sr.Microphone()
    text=''
    while text!='no' and text!='yes':
        with sr.Microphone() as source:
	    r.adjust_for_ambient_noise(source)
	    print("Listening...")
	    audio = r.listen(source, timeout=15)
	print("Got it, you said...")
	try:
	    text=r.recognize_google(audio)
	    print(text)
	except sr.UnknownValueError:
	    talk('try again')
	except sr.RequestError:
	    talk('try again')
    return audio

def check_answer(token):
	if (token == 'yes') or (token == 'Yes'):
		answer=True
		return answer
	else:
		answer=False
		return answer

def scan_prescription():
	global pub
	talk('Please place your prescription in the frame below')
    # publish scanning to OCR
	SPR_msg = SPR_message()
	SPR_msg.Scan = "START_OCR"
	pub.publish(SPR_msg)

def interact(data):
	global face_pub
	face_msg = Face_message()
	if data.NHSNumber == 0:   # person unrecognised
		face_msg.display = 'confused'
		face_pub.publish(face_msg)
		talk('Dont recognise you, do you have a paper prescription?')
		rospy.loginfo("Unknown person")
		audio = listen()
		face_msg.display = 'happy'
		face_pub.publish(face_msg)
#expected_audio=nlp(u"yes")	
		paper_prescription=check_answer(audio)
		if paper_prescription:
			scan_prescription()
#else
# publish--useless person

	else:  #person recognised
		face_msg.display = 'happy'
		face_pub.publish(face_msg)
		talk('Hello, hold on a second while we retrieve your medicines') 	
# ignore now--check if its in stock or not
# ignore now--if they have any medicines or not	


def main():
	global pub
	global face_pub
	rospy.init_node('greeting', anonymous=False)
	rospy.Subscriber("FR_DB_Channel", FR_message, interact) 
	pub = rospy.Publisher("SPR_OCR_Channel", SPR_message, queue_size=10)
	face_pub = rospy.Publisher("Face_Channel", Face_message, queue_size=10)
	rospy.spin()

if __name__ == '__main__':
	main()
