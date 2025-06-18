import datetime
import json
import os
import random
import webbrowser
from groq import Groq  # New import

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

# Remove Gemini configurations and add Groq
GROQ_API_KEY = "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"
groq_client = Groq(api_key=GROQ_API_KEY)

# ------------------- Functions -------------------

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Try voices[1].id for female voice
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    api_key = "1cb5f89b2ce24ff28cb7b8be0154114d"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
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

def get_ai_response(prompt):
    """Get AI response using Groq API"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis, a helpful AI assistant. Keep responses concise and natural."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            stream=False,
            temperature=0.7,
            max_tokens=500
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return "Sorry, I'm having trouble accessing my knowledge right now."

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

# ------------------- Main Assistant -------------------

def run_jarvis():
    speak("Hi! I am your assistant. How can I help you today?")
    
    while True:
        command = listen()

        if 'open youtube' in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'search' in command:
            speak("What do you want to search?")
            query = listen()
            if query:
                speak(f"Searching for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")

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
            # Handle explicit questions
            question = command
            for phrase in ['what is', 'who is', 'tell me about', 'explain', 'why']:
                if phrase in command:
                    question = command.replace(phrase, '').strip()
                    break
            
            if question:
                speak("Let me think about that...")
                answer = get_ai_response(question)
                speak(answer)
            else:
                speak("What would you like to know about?")

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye! Have a great day.")
            break

        elif command and len(command) > 3:
            # Handle any other input as a potential knowledge query
            # Skip very short commands or empty strings
            if not any(action in command for action in ['open', 'search', 'weather', 'date', 'time', 'joke']):
                speak("Let me find information about that...")
                answer = get_ai_response(command)
                speak(answer)
        
        elif command:
            speak("Sorry, I didn't catch that. Can you repeat?")

# ------------------- Entry Point -------------------

if __name__ == '__main__':
    run_jarvis()
