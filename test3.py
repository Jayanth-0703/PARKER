import datetime
import json
import os
import random
import urllib.parse
import webbrowser
from groq import Groq

import pyjokes
import pyttsx3
import requests
import speech_recognition as sr

# ------------------- Configurations -------------------

MOTIVATIONAL_QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal. - Winston Churchill",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
]

# Initialize Groq
GROQ_API_KEY = "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"
groq_client = Groq(api_key=GROQ_API_KEY)

# Weather API
WEATHER_API_KEY = "1cb5f89b2ce24ff28cb7b8be0154114d"

# Common websites
COMMON_WEBSITES = {
    'facebook': 'facebook.com',
    'youtube': 'youtube.com',
    'google': 'google.com',
    'twitter': 'twitter.com',
    'instagram': 'instagram.com',
    'linkedin': 'linkedin.com',
    'reddit': 'reddit.com',
    'amazon': 'amazon.com',
    'netflix': 'netflix.com',
    'github': 'github.com',
    'gmail': 'gmail.google.com',
    'outlook': 'outlook.live.com',
    'wikipedia': 'wikipedia.org',
    'pinterest': 'pinterest.com',
    'spotify': 'spotify.com'
}

# Add this near other configurations
MAX_HISTORY = 10  # Number of messages to remember

# ------------------- Helper Functions -------------------

def speak(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {str(e)}")

def listen():
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
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, the speech service is down.")
            return ""

def search_web(query):
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error searching web: {str(e)}")
        return False

def open_website(command):
    try:
        cleaned = command.lower()
        for word in ['open', 'website', 'go to', 'goto', 'visit', 'browse', 'dot com']:
            cleaned = cleaned.replace(word, '')
        cleaned = cleaned.strip().replace(' ', '')

        # If it's a common website name
        for name, url in COMMON_WEBSITES.items():
            if name in cleaned:
                cleaned = url
                break
        else:
            # Add .com if not already present
            if not any(ext in cleaned for ext in ['.com', '.org', '.net', '.edu', '.gov']):
                cleaned = f"{cleaned}.com"

        # Build final URL
        if not cleaned.startswith(('http://', 'https://')):
            cleaned = f"https://www.{cleaned}"

        print(f"Opening URL: {cleaned}")
        webbrowser.open(cleaned)
        speak(f"Opening {cleaned.replace('https://www.', '').replace('https://', '')}")
        return True
    except Exception as e:
        print(f"Error opening website: {str(e)}")
        speak("Sorry, I couldn't open that website.")
        return False

def get_weather(city):
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

def get_ai_response(prompt, conversation_history=[]):
    """Get AI response using Groq API with conversation history"""
    try:
        # Build messages list with conversation history
        messages = [
            {"role": "system", "content": "You are Parker, a helpful AI assistant. Keep responses concise and natural."}
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            stream=False,
            temperature=0.7,
            max_tokens=500
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return "Sorry, I'm having trouble accessing my knowledge right now."

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
