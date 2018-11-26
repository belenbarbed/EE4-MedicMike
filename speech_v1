import spacy
import pyaudio
import speech_recognition as sr

import pyttsx
import pyttsx
engine = pyttsx.init()

nlp=spacy.load('en_core_web_sm')
def check_semantics(answer):
    for token in answer:
         #is the token part of a stop list, ie. most common words of the language?
        if token.pos_ == 'INTJ':
            expected_word=True
            print("Expected answer \n")
        else:
            expected_word=False
            print("Not expected, try again please\n")

def check_answer(answer):
    for token in answer:
        if (token.text == 'yes') or (token.text == 'Yes'):
            answer=True
            return answer
        else:
            print("Why are you here then?")
            answer=False
            return answer

def listen():
	r=sr.Recognizer()
	sr.Microphone()
	with sr.Microphone() as source:
	    r.adjust_for_ambient_noise(source)
	    print("Listening...")
	    audio = r.listen(source, timeout=10)

	print("Got it, you said...")
	text=r.recognize_google(audio)
	print(text)


#speech production 
engine.say('Hello, are you here to pick up your prescription medicines? Yes/no')
engine.runAndWait()

#collect audio
#expected_audio=listen()
expected_audio=nlp(u"yes")  # simpler case scenario to the yes/no question. train for diff. cases
check_semantics(expected_audio)  # check to see if answer is semantically correct
medicine_required=check_answer(expected_audio) # check character of answer


if medicine_required:
    #speech production
    engine.say('Do you have a paper prescription? yes or no')
    engine.runAndWait()
 
    #collect audio
    audio=listen()
    paper_prescription=check_answer(expected_audio) #true if paper

    # stop

if paper_prescription:
    engine.say('Please place it within the frame, so I can scan the documen')  # speech production 
    engine.runAndWait()
    # ** Query OCR to see if letter has been detected		
    # if letter_detected
    engine.say('Hold on a second, the prescription is being scanned')  # speech production
    engine.runAndWait()
    # elif
    engine.say('Please place the prescription within the frame')
    engine.runAndWait()

    # ** Query OCR to see if prescription drug has been recognised
    # if scan_success  
    engine.say('Youre prescription medicine will arrive shortly')
    engine.runAndWait()
    # elif
    engine.say('Please try again')
    engine.runAndWait()

if paper_prescription==False:
    #check Face ID
    if faceID == "unknown":
        engine.say('Dont recognise you from previous times, can we register your FACE ID for the   next times?, (yes/ no)')
        engine.runAndWait()
        #collect audio
        audio=listen()
	    #if audio==yes
		# MESSAGE FR TO TAKE PICTURE
		# QUERY FR if FACE ID has been registered
		#engine.say('Your face ID has been registered')
		#engine.runAndWait()
		# MESSAGE OCR TO SCAN ID
		# QUERY OCR if ID is valid
                #engine.say('Your ID has been scanned successfully')
		#engine.runAndWait()
		# if ID matches:
		# speech production
		#engine.say('your drugs will be arriving shortly')
		#engine.runAndWait()
		# elif ID matches !=
		#     engine.say('Your ID is invalid')
		#     engine.runAndWait()
		# ** QUERY OCR TO SCAN ID AGAIN
            #else
	        #engine.say('We wont record your face, the next times you come you will need to show your ID for verification purposes')
    elif faceID == "known":
        #speech production
        engine.say('Hey, hold on for a second while we retrive your meds')
     
	# QUERY DATABASE
    #elif error:
	# deal with it	


