#!/usr/bin/env python
import rospy

import spacy  # speech processing API
import pyaudio # importing audio from microphone
import speech_recognition as sr # Speech-To-Text library
import pyttsx
from gtts import gTTS
from mm_spr.msg import FR_message  
from mm_spr.msg import SPR_message  
from mm_spr.msg import Face_message
from mm_spr.msg import OCR_message  
import os
nlp = spacy.load('en_core_web_sm')

def talk(phrase):
	# engine = pyttsx.init()

	# engine.setProperty('voice', 'scottish')
	# engine.say(phrase)
	# engine.runAndWait()
	# tts = gTTS(text=phrase, lang='en')
	# tts.save("speech.mp3")
	# os.system("mpg321 speech.mp3")
	try:
		tts = gTTS(text=phrase, lang='en')
		tts.save("speech.mp3")
		os.system("mpg321 speech.mp3")
	except:
		rospy.loginfo('Failed GTTS')
		engine = pyttsx.init()
		engine.say(phrase)
		engine.runAndWait()

def listen():
    r=sr.Recognizer()
    sr.Microphone(device_index=6)
    text=''
    while text!='no' and text!='yes':
        with sr.Microphone(device_index=6) as source:
	    r.adjust_for_ambient_noise(source)
	    print("Listening...")
	    audio = r.listen(source, timeout=10)
	    print("Got it, you said...")
	text = ""
	while text == "":
	    try:
	        text=r.recognize_google(audio)
	        print(text)
	    except sr.UnknownValueError:
	        talk('try again. Please say yes or no.')
	    except sr.RequestError:
	        talk('try again. Please say yes or no.')
	return text

def check_answer(text):
	if (text == 'yes') or (text == 'Yes'):
		answer=True
		return answer
	else:
		answer=False
		return answer

def scan_prescription():
	global pub
	#talk('Please scan the barcode on your prescription')
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
		talk('Dont recognise you, please scan the barcode on your prescription')
		rospy.loginfo("Unknown person")
		#audio = listen()
		face_msg.display = 'happy'
		face_pub.publish(face_msg)
#expected_audio=nlp(u"yes")	
		#paper_prescription=check_answer(audio)
		#rospy.loginfo(str(paper_prescription))
		if True:
			scan_prescription()
#else
# publish--useless person

	else:  #person recognised
		face_msg.display = 'happy'
		face_pub.publish(face_msg)
		talk('Hello, hold on a second while we retrieve your medicines') 	
# ignore now--check if its in stock or not
# ignore now--if they have any medicines or not	

def collecting(data):
    meds = data.Prescription_Info
    sts = "I'm just getting your" + str(meds) + "for you. Please wait a moment"
    talk(sts)
def main():
	global pub
	global face_pub
	rospy.init_node('greeting', anonymous=False)
	rospy.Subscriber("FR_DB_Channel", FR_message, interact)
	rospy.Subscriber("OCR_DB_Channel", OCR_message, collecting) 
	pub = rospy.Publisher("SPR_OCR_Channel", SPR_message, queue_size=10)
	face_pub = rospy.Publisher("Face_Channel", Face_message, queue_size=10)
	rospy.spin()

if __name__ == '__main__':
    main()
