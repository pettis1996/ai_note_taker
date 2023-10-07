import os
import time 
import pyaudio
import playsound
from gtts import gTTS
import openai
import speech_recognition as sr
import pyautogui
import pytesseract
from PIL import Image


api_key = "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"
lang = "en"
openai.api_key = api_key

guy = ""
microphone = sr.Microphone()

def play_audio(text):
    speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
    speech.save("output.mp3")
    playsound.playsound("output.mp3")
    print("=======")
    print("HERE")
    print("=======")

def get_audio():
    r = sr.Recognizer()
    with microphone as source:
        audio = r.listen(source)
        said = ""
        print("=======")
        print(said)
        print("=======")

        try:
            said = r.recognize_google(audio)
            print(said)
            global guy
            guy = said

            if "go" in said:
                play_audio("I am sorry")
            elif "Friday" in said: 
                new_string = said.replace("Friday", "")
                print(new_string)
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_string}])
                text = completion.choises[0].message.content
                play_audio(text)
        except Exception as e:
            print("Exception:", str(e))

while True:
    if "stop" in guy:
        break
    get_audio()