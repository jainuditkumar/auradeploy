import streamlit as st
import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install SpeechRecognition, PyAudio, setuptools
import os  # part of standard python library
import webbrowser  # part of standard python library
import subprocess  # part of standard python library
import datetime  # part of standard python library
import wikipedia  # pip install wikipedia
import requests  # allows us to use external APIs
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import asyncio
import platform
from g4f.client import Client  # pip install -U g4f
from g4f.Provider import You

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Initialize the G4F client
client = Client(provider=You)

# Function to convert text to speech
def say(text):
    st.write(f"🤖: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to take voice commands
def take_command():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            say("I am Listening...")
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio)
                st.write(f"👨: {query}")
                return query
            except Exception as e:
                r = sr.Recognizer()
                continue

# Streamlit app
def main():
    st.title("Aura AI")
    st.write("Hello, I am Aura AI")

    query = st.text_input("Enter your command:", "")
    if st.button("Submit"):
        process_query(query)

def process_query(query):
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"],
        ["chatgpt", "https://chat.openai.com/"]
    ]

    if "open" in query.lower():
        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])
    elif "google" in query.lower():
        say("Web search for the same has been opened in browser")
        URL = "https://www.google.co.in/search?q=" + query
        webbrowser.open(URL)
    elif "image" in query.lower() or "picture" in query.lower():
        say("Web search for the same has been opened in browser")
        URL = "https://yandex.com/images/search?text=" + query
        webbrowser.open(URL)
    elif "time" in query.lower():
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        say(f"The time is {hour}:{min}")
    elif "weather" in query.lower():
        cityname = query.split("of")[-1].strip()
        say("Please wait a moment...")
        weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&units=imperial&APPID=253682c0bd759acfb4255d4aa08c3dd7")
        data = weather_data.json()
        main = data['main']
        temperature = main['temp']
        humidity = main['humidity']
        pressure = main['pressure']
        say(f"Temperature is {round((temperature-32)*5/9, 2)}°C")
        say(f"Humidity is {humidity}%")
        say(f"Pressure is {pressure} hPa")
    elif "who" in query.lower() or "what" in query.lower():
        URL = "https://www.google.co.in/search?q=" + query
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
        }
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all(class_='Z0LcW')
        if results:
            for result in results:
                say(result.get_text())
        else:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}]
            )
            response = chat_completion.choices[0].message.content
            say(response)
    elif "shutdown" in query.lower():
        say("Are you sure?")
        temp = st.text_input("Confirm shutdown (y/n):")
        if temp.lower() in ["y", "yes"]:
            say("Thanks for talking to me")
            say("Immediate shutdown taking place")
            os.system("shutdown /s /t 5")
            say("Exiting now")
        else:
            say("I'm ready to talk to you again!")
    elif "calculator" in query.lower():
        say("Opening Calculator")
        subprocess.Popen("C:\\Windows\\System32\\calc.exe")
    elif "quit" in query.lower() or "bye" in query.lower():
        say("Thanks for using me. Wishing you a good day ahead!")
    else:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )
        response = chat_completion.choices[0].message.content
        say(response)

if __name__ == '__main__':
    main()
