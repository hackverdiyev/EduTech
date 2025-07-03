import speech_recognition as sr
import pywhatkit
import pyaudio
import pyttsx3
import openai
import os

openai.api_key="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"

def get_audio():
    mic = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            mic.adjust_for_ambient_noise(source, duration=0.2)
            print("Say something...")
            audio = mic.listen(source)

        text = mic.recognize_google(audio)
        return text
    except: 
        mic = sr.Recognizer()

text = get_audio()

print("Got the text")

text=openai.ChatCompletion.create(model='gpt-3.5-turbo',messages=[{'role':'user','content':text}])
text=text["choices"][0]["message"]["content"]

engine=pyttsx3.init()
engine.setProperty("rate", 150)
voices = engine.getProperty('voices')  
engine.setProperty('voice', voices[1].id)
engine.say(text)
engine.runAndWait()


