import os
import time 
import pyaudio
import pygame.mixer
import playsound
from gtts import gTTS
import openai
import speech_recognition as sr
import pyautogui
import pytesseract
from PIL import Image
import dotenv

dotenv.load_dotenv()

api_key = os.environ['API_KEY'] # OpenAI API KEY from the .env file
lang = "en"                     # [en, el]
openai.api_key = api_key

guy = ""
microphone = sr.Microphone()

pygame.mixer.init()

def play_audio(text):
    speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
    speech.save("output.mp3")
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def create_note_file(note: str, file_path: str):
    with open(file_path, "a") as f:
        f.write(note + "\n")

def get_audio():
    r = sr.Recognizer()
    with microphone as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
            global guy
            guy = said

            if "note" in said: 
                print("Opening note file...")
                play_audio("What would you like to make a note for?")
                note_audio = r.listen(source)
                note = r.recognize_google(note_audio)
                print("Note Saved!")
                play_audio("Note was successfully saved!")
                file_path = os.path.expanduser("~/Desktop/Notes.txt")
                create_note_file(note, file_path)
                while True:
                    play_audio("Would you like to save another note?")
                    another_note_audio = r.listen(source)
                    response = r.recognize_google(another_note_audio)
                    if "yes" in response:
                        play_audio("Would you like to add to the existing note?")
                        note_audio = r.listen(source)
                        note = r.recognize_google(note_audio)
                        create_note_file(note, file_path)
                        play_audio("The note was saved again!")
                    else:
                        break
            elif "go" in said:
                play_audio("Note Bot Enabled. What can I do for you? Remember say Please first!")
            elif "Please" in said: 
                new_string = said.replace("Please", "")
                print(new_string)
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_string}])
                text = completion["choices"][0]["message"]["content"]
                play_audio(text)
        except Exception as e:
            print("Exception:", str(e))

while True:
    if "stop" in guy:
        break
    get_audio()