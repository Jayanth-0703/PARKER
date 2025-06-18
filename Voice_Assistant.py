import datetime
import os
import urllib.parse
import webbrowser

import pyjokes
import pyttsx3
import speech_recognition as sr


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

def run_jarvis():
    speak("Hi! I am your assistant. How can I help you today?")
    while True:
        command = listen()

        if 'open youtube' in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'search for' in command:
            # Extract query directly from command
            query = command.replace('search for', '').strip()
            if query:
                speak(f"Searching for {query}")
                search_web(query)

        elif 'open' in command:
            # Extract site name, removing common words
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

        elif command:
            speak("Sorry, I didn't catch that. Can you repeat?")

if __name__ == '__main__':
    run_jarvis()
