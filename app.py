from flask import Flask, render_template, request, redirect
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from pygame import mixer
import time

class _TTS:

    engine = None
    rate = None

    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

    def start(self, text_):
        self.engine.say(text_)
        self.engine.runAndWait()


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# # print(voices[1].id)
# engine.setProperty('voice', voices[0].id)


def speak(audio):
    tts = _TTS()
    tts.start(audio)
    del(tts)


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Liberty Sir. Please tell me how may I help you")


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/greet')
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hi I am your voice assistance Sir. Please tell me how may I help you")

    return render_template('index.html')


@app.route('/command')
def Command():
    speak("Please tell your query sir")
    while True:
        # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
            return render_template('index.html')
           

        elif 'open youtube' in query:
            speak("Opening youtube in just a second sir!")
            webbrowser.get(chrome_path).open("youtube.com")
            return render_template('index.html')

        elif 'open google' in query:
            speak("Opening google.com in just a second sir")
            webbrowser.get(chrome_path).open("google.com")
            return render_template('index.html')

        elif 'open stack overflow' in query:
            speak("Opening Stack Overflow in just a second sir")
            webbrowser.get(chrome_path).open("stackoverflow.com")
            return render_template('index.html')

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            return render_template('index.html')

        elif 'open code' in query:
            speak("Opening Visual Studio Code Sir")
            codePath = "C:\\Users\\dell\\AppData\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            return render_template('index.html')

        elif 'play music' in query:
            speak("Playing music sir")
            mixer.init()
            mixer.music.load('water.mp3')
            mixer.music.play()
            time.sleep(20)
            mixer.music.stop()
            return render_template('index.html')

    


if __name__ == "__main__":
    app.run(debug=True, port=8000)
