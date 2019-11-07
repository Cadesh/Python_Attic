# check these sites:
# https://realpython.com/python-speech-recognition/
# https://www.code-learner.com/python-speech-recognition-introduction-and-practice/


# dependencies
# conda install -c menpo ffmpeg
# conda install -c conda-forge speechrecognition
# conda install -c conda-forge pydub

import speech_recognition as sr
from os import path
from pydub import AudioSegment

print("Start.")
BING_KEY = "cfee7d6db79d4671b9cea936da4689d7" 

# convert mp3 file to wav                                                       
sound = AudioSegment.from_mp3("churchill.mp3")
sound.export("transcript.wav", format="wav")

# use the audio file as the audio source                                        
r = sr.Recognizer()
with sr.AudioFile("transcript.wav") as source:
    audio = r.record(source)  # read the entire audio file 

try:
    transcribe = r.recognize_bing(audio, key=BING_KEY)                
    print("Transcription: " + audio)

except sr.UnknownValueError:
    print ('error')

    