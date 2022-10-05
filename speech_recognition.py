from psychopy import voicekey
import speech_recognition as sr
import time

record_length = 5 # Change the legnth of the recording here
voicekey.pyo_init(rate = 48000,buffersize=256) # Initialize some parameters
# Capture some audio
onset = voicekey.OnsetVoiceKey(sec = record_length, file_out='audio_file.wav',baseline = 10) # Check for voice onset
try: # This try except is needed for the baseline argument in the voice onset check
    onset.start()
except AttributeError:
    pass
time.sleep(record_length+2) # pause for a few seconds to make sure everything is captured
AUDIO_FILE = 'audio_file.wav'
r = sr.Recognizer() # Initialize the speech recognizer
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source) # Record the audio from microphone

# Audio onset
RT = onset.event_onset
# Use Google Speech Recognition to transcribe the audio
word_said = r.recognize_google(audio)
