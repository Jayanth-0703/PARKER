import datetime
import os
import urllib.parse
import webbrowser

import pyjokes
import pyttsx3
import speech_recognition as sr

# Add these imports at the top
from googletrans import Translator

# Add this dictionary after imports
LANGUAGE_CODES = {
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'italian': 'it',
    'portuguese': 'pt',
    'hindi': 'hi',
    'chinese': 'zh-cn',
    'japanese': 'ja',
    'korean': 'ko'
}

# Add this global variable at the top with other imports
current_language = 'english'

# Modify the speak function to use the current language
def speak(text):
    global current_language
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Get the language code for current language
        lang_code = LANGUAGE_CODES[current_language]
        
        # Try to find voice for current language
        for voice in voices:
            if lang_code in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # If text is not in current language, translate it
        if current_language != 'english':
            text = translate_text(text, lang_code)
            
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {str(e)}")
        # Fallback to English if there's an error
        engine.setProperty('voice', voices[0].id)
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

# Add these new functions
def change_language(new_language):
    """Change the assistant's speaking language"""
    global current_language
    try:
        if new_language.lower() in LANGUAGE_CODES:
            lang_code = LANGUAGE_CODES[new_language.lower()]
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # Try to find a voice for the requested language
            for voice in voices:
                if lang_code in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    current_language = new_language.lower()  # Update current language
                    return True, lang_code
            
            speak(f"Sorry, I couldn't find a voice for {new_language}")
            return False, None
        else:
            speak(f"Sorry, I don't support {new_language} yet")
            return False, None
    except Exception as e:
        print(f"Error changing language: {str(e)}")
        return False, None

def translate_text(text, target_lang):
    """Translate text to target language"""
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text

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

        elif any(phrase in command for phrase in ['change language', 'switch language', 'speak in', 'convert to']):
            # Extract language from command
            for lang in LANGUAGE_CODES.keys():
                if lang in command.lower():
                    speak(f"Switching to {lang}")
                    success, lang_code = change_language(lang)
                    if success:
                        welcome_msg = {
                            'spanish': '¡Hola! Ahora estoy hablando en español',
                            'french': 'Bonjour! Je parle maintenant en français',
                            'german': 'Hallo! Ich spreche jetzt Deutsch',
                            'italian': 'Ciao! Ora parlo in italiano',
                            'portuguese': 'Olá! Agora estou falando em português',
                            'english': 'Hello! I am now speaking in English'
                        }.get(lang, f"Hello! I am now speaking in {lang}")
                        speak(welcome_msg)
                    break
            else:
                speak("Please specify a supported language. I support: " + ", ".join(LANGUAGE_CODES.keys()))

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye! Have a great day.")
            break

        elif command:
            speak("Sorry, I didn't catch that. Can you repeat?")

if __name__ == '__main__':
    run_jarvis()
