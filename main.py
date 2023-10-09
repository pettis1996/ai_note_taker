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

user = ""
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

def read_note(file_path: str):
    with open(file_path, "r") as f:
        return f.readlines()
    
def capture_screenshot(file_path: str):
    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)

def get_audio():
    r = sr.Recognizer()
    with microphone as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
            global user
            user = said
            file_name = ""

            if "note" in said: 
                print("Preparing to write take a note...")
                play_audio("What would you like to make a note for?")
                note_audio = r.listen(source)
                note = r.recognize_google(note_audio)
                print(f"Note: \n{note}")
                file_name = "note"
                extension = ".txt"
                file_path = os.path.expanduser(f"~/Desktop/{file_name}{extension}")
                if os.path.exists(file_path):
                    file_counter = 1
                    while os.path.exists(file_path):
                        new_file_name = file_name + str(file_counter) + extension
                        file_path = os.path.expanduser(f"~/Desktop/{new_file_name}")
                        file_counter += 1
                play_audio(f"Note Saved as {file_name} on your Desktop!")
                print(f"Note Saved as {file_name} on {file_path}")
                create_note_file(note, file_path)
                while True:
                    play_audio("Would you like to take another note?")
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
                            file_name = "note"
                            play_audio("What would you like to take a note for?")
                            note_audio = r.listen(source)
                            note = r.recognize_google(note_audio)
                            file_path = os.path.expanduser(f"~/Desktop/{file_name}{extension}")
                            if os.path.exists(file_path):
                                file_counter = 1
                                while os.path.exists(file_path):
                                    new_file_name = file_name + str(file_counter)
                                    file_path = os.path.expanduser(f"~/Desktop/{new_file_name}{extension}")
                                    file_counter += 1
                            play_audio(f"Note Saved as {file_name} on your Desktop!")
                            print(f"Note Saved as {file_name} on {file_path}")
                            create_note_file(note, file_path)
                    else:
                        print("DONE.")
                        break
            elif "Reed" in said:
                play_audio("What file should I read from?")
                file_name_prompt = r.listen(source)
                file_name = r.recognize_google(file_name_prompt)
                file_path = os.path.expanduser(f"~\Desktop\{file_name}.txt")
                file_lines = read_note(file_path)
                for line in file_lines:
                    clean_line = line.replace("\n", "")
                    play_audio(clean_line)
                play_audio(f"End of file {file_name}")
            elif "go" in said:
                play_audio("Note Bot Enabled. What can I do for you? Remember say Please first for using ChatGPT!")
            elif "Please" in said: 
                new_string = said.replace("Please", "")
                print(new_string)
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_string}])
                text = completion["choices"][0]["message"]["content"]
                play_audio(text)
            elif "screenshot" in said:
                print("Taking a screenschot...")
                screenshot_dir = os.path.expanduser("~/Desktop")
                file_name = "screenshot"
                extension = ".png"
                file_path = os.path.join(screenshot_dir, file_name + extension)

                if os.path.exists(file_path):
                    file_counter = 1
                    while os.path.exists(file_path):
                        new_filename = file_name + str(file_counter) + extension
                        file_path = os.path.join(screenshot_dir, new_filename)
                        file_counter += 1

                capture_screenshot(file_path)
                play_audio("Screenshot saved!")
        except Exception as e:
            print("Exception:", str(e))

while True:
    if "stop" in user:
        break
    get_audio()