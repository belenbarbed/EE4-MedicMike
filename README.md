# EE4-PostBotPat
HCR Coursework 2018

Dependencies
- SpeechRecognition and speechrecognition.google, the wrapper for the Google Cloud API to transcribe speech into text.
- SpaCy, the natural language processing API used to understand the content of speech
- pttsx, the speech-to-text library that syntheses speech

The first two sub-systems require internet connectivity, whereas pttsx does not. Note that Google Cloud also offers as text-to-speech library which could have been used, though because it connects to the cloud and the difference in performance to pttsx is undetermined, the latter was chosen. 

