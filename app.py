import streamlit as st 
import requests
from bs4 import BeautifulSoup
import datetime
import webbrowser
import wikipedia
from g4f.client import Client
from g4f.Provider import You
import asyncio
 

# Initialize the G4F client
client = Client(provider=You)

# Function to convert text to speech
def say(text):
    st.write(f"🤖: {text}") 

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
            try:
                chat_completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": query}]
                )
                response = chat_completion.choices[0].message.content
                say(response)
            except Exception as e:
                st.error(f"Error processing query: {e}")
    elif "shutdown" in query.lower():
        say("Shutdown functionality is not supported on Streamlit Cloud.")
    elif "calculator" in query.lower():
        say("Opening Calculator is not supported on Streamlit Cloud.")
    elif "quit" in query.lower() or "bye" in query.lower():
        say("Thanks for using me. Wishing you a good day ahead!")
    else:
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}]
            )
            response = chat_completion.choices[0].message.content
            say(response)
        except Exception as e:
            st.error(f"Error processing query: {e}")

if __name__ == '__main__':
    main()
