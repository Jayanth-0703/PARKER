import datetime
import json
import os
import random
import urllib.parse
import webbrowser
from typing import Any, Dict, List, Optional

import pyjokes
import pyttsx3
import requests
import speech_recognition as sr
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam

# ------------------- Configurations -------------------
MAX_HISTORY = 5  # Number of messages to remember

MOTIVATIONAL_QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal. - Winston Churchill",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
]

# Initialize API Keys
GROQ_API_KEY = "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"
WEATHER_API_KEY = "1cb5f89b2ce24ff28cb7b8be0154114d"

groq_client = Groq(api_key=GROQ_API_KEY)

# ------------------- Voice Functions -------------------
def speak(text: str) -> None:
    """Convert text to speech"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {str(e)}")

def listen() -> str:
    """Listen for voice input"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("🧠 Recognizing...")
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an error with the speech service.")
            return ""

# ------------------- AI Functions -------------------
def get_ai_response(
    prompt: str, conversation_history: Optional[List[Dict[str, str]]] = None
) -> str:
    """Get AI response using Groq API with conversation history"""
    if conversation_history is None:
        conversation_history = []

    try:
        messages: List[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": "You are Parker, an AI assistant created by Jayanth. You're helpful, knowledgeable, and maintain context from previous messages. Keep responses concise and natural.",
            }
        ]

        # Add conversation history
        for message in conversation_history:
            if isinstance(message, dict) and "role" in message and "content" in message:
                messages.append(message)

        # Add current prompt
        messages.append({"role": "user", "content": prompt})

        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            stream=False,
            temperature=0.7,
            max_tokens=500,
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return "Sorry, I'm having trouble accessing my knowledge right now."


# ------------------- Utility Functions -------------------
def get_weather(city):
    """Get weather information for a city"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = round(data["main"]["temp"])
            desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            return f"The temperature in {city} is {temp}°C with {desc}. The humidity is {humidity}%"
        else:
            return f"Sorry, I couldn't find the weather for {city}."
    except Exception as e:
        print("Weather error:", str(e))
        return "Sorry, there was an error getting the weather information."


def get_random_content(category):
    """Get random content based on category"""
    try:
        if category in ["motivation", "quote"]:
            try:
                url = "https://zenquotes.io/api/random"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    return f"Here's a quote: {data[0]['q']} - by {data[0]['a']}"
            except:
                return f"Here's a quote: {random.choice(MOTIVATIONAL_QUOTES)}"
        elif category == "fact":
            url = "https://uselessfacts.jsph.pl/random.json?language=en"
            response = requests.get(url)
            if response.status_code == 200:
                return f"Here's a random fact: {response.json()['text']}"
        elif category == "joke":
            return pyjokes.get_joke()
        return f"Sorry, I couldn't find any {category} right now."
    except Exception as e:
        print("Content error:", str(e))
        return f"Sorry, I had trouble getting {category}."


def play_music(command):
    """Handle music playback requests"""
    try:
        query = command.lower()
        for word in ["play", "song", "music", "on", "in"]:
            query = query.replace(word, "")
        query = query.strip()

        if 'spotify' in command.lower():
            platform = 'spotify'
            url = f"https://open.spotify.com/search/{urllib.parse.quote(query)}"
        elif 'soundcloud' in command.lower():
            platform = 'soundcloud'
            url = f"https://soundcloud.com/search?q={urllib.parse.quote(query)}"
        else:
            platform = 'youtube music'
            url = f"https://music.youtube.com/search?q={urllib.parse.quote(query)}"

        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error playing music: {str(e)}")
        return False


def search_web(query):
    """Search the web using Google"""
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error searching web: {str(e)}")
        return False


def open_website(command):
    """Open any website"""
    try:
        site = command.lower().strip()
        words_to_remove = [
            "website",
            "open",
            "goto",
            "go to",
            "visit",
            "browse",
            "www.",
            "http://",
            "https://",
        ]
        for word in words_to_remove:
            site = site.replace(word, "").strip()

        # Add domain extension if missing
        if not any(ext in site for ext in [".com", ".org", ".net", ".edu", ".gov"]):
            site = f"{site}.com"

        # Ensure proper URL format
        if not site.startswith(("http://", "https://")):
            site = f"https://{'www.' if not site.startswith('www.') else ''}{site}"

        webbrowser.open(site)
        return True
    except Exception as e:
        print(f"Error opening website: {str(e)}")
        return False

# ------------------- Main Function -------------------

def run_parker():
    speak("Hi! I am Parker, your AI assistant. How can I help you today?")
    conversation_history = []
    
    while True:
        command = listen()

        if not command:
            continue

        if 'open youtube' in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'search for' in command:
            query = command.replace('search for', '').strip()
            if query:
                speak(f"Searching for {query}")
                search_web(query)

        elif 'open file' in command:
            speak("Please tell the full path of the file")
            print("Say something like: C drive users desktop file dot txt")
            filepath = listen().replace(" ", "\\").replace("dot", ".")
            try:
                os.startfile(filepath)
                speak("Opening file")
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open the file. Please check the path.")

        elif any(word in command for word in ['play', 'song', 'music']):
            play_music(command)

        elif 'open' in command:
            open_website(command)

        elif 'date' in command:
            today = datetime.date.today().strftime("%B %d, %Y")
            speak(f"Today's date is {today}")

        elif 'time' in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")

        elif 'weather' in command:
            city = None
            if 'in' in command:
                city = command.split('in')[-1].strip()
            if not city:
                speak("Which city would you like to know the weather for?")
                city = listen()
            if city:
                speak(get_weather(city))
            else:
                speak("I couldn't understand the city name. Please try again.")

        elif any(word in command for word in ['motivation', 'quote', 'fact', 'joke']):
            category = next(word for word in ['motivation', 'quote', 'fact', 'joke'] if word in command)
            speak(get_random_content(category))

        elif any(word in command for word in ['what is', 'who is', 'tell me about', 'explain', 'why']):
            question = command
            for phrase in ['what is', 'who is', 'tell me about', 'explain', 'why']:
                if phrase in command:
                    question = command.replace(phrase, '').strip()
                    break
            if question:
                speak("Let me think about that...")
                answer = get_ai_response(question, conversation_history)
                speak(answer)
                
                # Update conversation history
                conversation_history.append({"role": "user", "content": question})
                conversation_history.append({"role": "assistant", "content": answer})
                
                # Limit history size
                if len(conversation_history) > MAX_HISTORY * 2:  # *2 because each exchange has 2 messages
                    conversation_history = conversation_history[-MAX_HISTORY * 2:]
            else:
                speak("What would you like to know about?")

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye! Have a great day.")
            break

        elif len(command) > 3:
            if not any(action in command for action in ['open', 'search', 'weather', 'date', 'time', 'joke']):
                speak("Let me find information about that...")
                answer = get_ai_response(command, conversation_history)
                speak(answer)
                
                # Update conversation history
                conversation_history.append({"role": "user", "content": command})
                conversation_history.append({"role": "assistant", "content": answer})
                
                # Limit history size
                if len(conversation_history) > MAX_HISTORY * 2:
                    conversation_history = conversation_history[-MAX_HISTORY * 2:]

        else:
            speak("Sorry, I didn't catch that. Can you repeat?")

if __name__ == '__main__':
    run_parker()
