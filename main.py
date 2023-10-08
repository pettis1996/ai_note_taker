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
    pygame.mixer.music.unload()

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
            file_name = ""

            if "note" in said: 
                print("Preparing to write take a note...")
                play_audio("What would you like to make a note for?")
                note_audio = r.listen(source)
                note = r.recognize_google(note_audio)
                play_audio("What should I name the file?")
                file_name_prompt = r.listen(source)
                file_name = r.recognize_google(file_name_prompt)
                play_audio(f"Note Saved as {file_name} on your Desktop!")
                file_path = os.path.expanduser(f"~/Desktop/{file_name}")
                print(f"Note Saved as {file_name} on {file_path}")
                create_note_file(note, file_path)
                while True:
                    play_audio("Would you like to save another note?")
                    another_note_audio = r.listen(source)
                    response = r.recognize_google(another_note_audio)
                    if "yes" in response:
                        play_audio("Would you like to add to the existing note?")
                        note_audio = r.listen(source)
                        response = r.recognize_google(note_audio)
                        if "yes" in response:
                            play_audio("What would you like to take a note for?")
                            note_audio = r.listen(source)
                            note = r.recognize_google(note_audio)
                            create_note_file(note, file_path)
                            play_audio("The note was added and saved!")
                        else:
                            play_audio("What should I name the new file?")
                            file_name_prompt = r.listen(source)
                            file_name = r.recognize_google(file_name_prompt)
                            play_audio("What would you like to take a note for?")
                            note_audio = r.listen(source)
                            note = r.recognize_google(note_audio)
                            play_audio(f"Note Saved as {file_name} on your Desktop!")
                            file_path = os.path.expanduser(f"~/Desktop/{file_name}")
                            print(f"Note Saved as {file_name} on {file_path}")
                            create_note_file(note, file_path)
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