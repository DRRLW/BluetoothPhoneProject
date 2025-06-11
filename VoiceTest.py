import openai
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voices[8].id)
   engine.setProperty('rate',170)

   engine.say('Hi, it is nice to meet you, my friend.')
engine.runAndWait()
'''
for voice in voices:
    engine.setProperty('voice', voice.id)
    print(f"Now using: {voice.name} - {voice.id}- {voice.age}- {voice.gender}")
    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()'''
