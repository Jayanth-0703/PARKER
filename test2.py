import datetime
import os
import urllib.parse
import webbrowser

import pyjokes
import pyttsx3
import speech_recognition as sr
from openai import OpenAI


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # You can try voices[1].id for a female voice
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

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
    """Search the web using Google"""
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error searching web: {str(e)}")
        return False

def open_website(site):
    """Open any website"""
    try:
        # Clean up the site name and remove extra words
        site = site.lower().strip()
        site = site.replace('www.', '').replace('http://', '').replace('https://', '')
        site = site.replace('website', '').replace('open', '').strip()
        
        # Check if site already contains a domain extension
        if any(ext in site for ext in ['.com', '.org', '.net', '.edu', '.gov']):
            url = f"https://www.{site}"
        else:
            url = f"https://www.{site}.com"
        
        webbrowser.open(url)
        speak(f"Opening {site}")
        return True
    except Exception as e:
        print(f"Error opening website: {str(e)}")
        return False

# Update the OpenAI client initialization with error handling
def initialize_openai():
    try:
        client = OpenAI(api_key="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")
        return client
    except Exception as e:
        print(f"Error initializing OpenAI: {str(e)}")
        return None

# Update the get_ai_response function
def get_ai_response(prompt, client):
    """Get response from OpenAI"""
    if not client:
        return "Sorry, AI service is not available."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant. Keep responses concise and natural."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return "Sorry, I'm having trouble thinking right now."

# Modify the run_jarvis() function to include conversational AI
def run_jarvis():
    ai_client = initialize_openai()
    conversation_history = []
    speak("Hi! I am Jarvis, your AI assistant. How can I help you today?")
    
    while True:
        command = listen()
        
        if command:
            conversation_history.append({"role": "user", "content": command})

        if 'open youtube' in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'search for' in command:
            # Extract query directly from command
            query = command.replace('search for', '').strip()
            if query:
                speak(f"Searching for {query}")
                search_web(query)

        elif 'open' in command and any(ext in command for ext in ['website', '.com', '.org', '.net']):
            site = command.replace('open', '').strip()
            site = site.replace('website', '').replace('dot com', '.com').strip()
            if site:
                open_website(site)

        elif 'open file' in command:
            speak("Please tell the full path of the file")
            print("You can say something like: C drive users documents file dot txt")
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
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time}")

        elif 'joke' in command:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye! Have a great day.")
            break

        elif command and len(command) > 3:
            # Use AI for general conversation
            full_prompt = "\n".join([msg["content"] for msg in conversation_history[-3:]])
            response = get_ai_response(full_prompt, ai_client)
            speak(response)
            
            # Add AI response to conversation history
            conversation_history.append({"role": "assistant", "content": response})
            
            # Limit history size
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]

if __name__ == '__main__':
    run_jarvis()
