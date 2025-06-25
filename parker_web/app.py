import datetime
import os
import sys

import pyttsx3
from flask import Flask, jsonify, render_template, request, session

# Add parent directory to Python path to import Parker functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from final import (
    get_ai_response,
    get_random_content,
    get_weather,
    open_website,
    play_music,
    search_web,
)

app = Flask(__name__)
app.secret_key = 'parker-ai-secret-key'  # Required for session management
MAX_HISTORY = 5  # Number of messages to remember

@app.before_request
def before_request():
    if 'conversation_history' not in session:
        session['conversation_history'] = []

def speak_text(text):
    """Synthesize text to speech"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception as e:
        print(f"Speech error: {str(e)}")
        return False

@app.route('/')
def home():
    try:
        # Test speech synthesis at startup
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        return render_template('index.html')
    except Exception as e:
        return render_template('index.html', error=f"Speech synthesis not available: {str(e)}")

# Update the system message in get_ai_response or where you initialize the assistant
SYSTEM_MESSAGE = """You are Parker, a helpful AI assistant created by Jayanth. 
When asked about your creator or who made you, always mention Jayanth as your creator.
Keep responses concise and natural."""

@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.json
    command = data.get('command', '').lower()
    conversation_history = session.get('conversation_history', [])
    response = {'status': 'success', 'response': None, 'action': None}

    try:
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response['response'] = f"The time is {current_time}"
            speak_text(response['response'])

        elif 'date' in command:
            today = datetime.date.today().strftime("%B %d, %Y")
            response['response'] = f"Today's date is {today}"
            speak_text(response['response'])

        elif 'creator' in command or 'who made you' in command or 'who created you' in command:
            response['response'] = "I'm Parker, created by Jayanth. I'm here to help you with various tasks and answer your questions!"
            speak_text(response['response'])

        elif any(word in command for word in ['what is', 'who is', 'tell me about', 'explain', 'why', 'when']):
            # Get AI response with conversation history
            ai_response = get_ai_response(command, conversation_history)
            response['response'] = ai_response
            speak_text(ai_response)
            
            # Update conversation history
            conversation_history.append({"role": "user", "content": command})
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Limit history size
            if len(conversation_history) > MAX_HISTORY * 2:
                conversation_history = conversation_history[-MAX_HISTORY * 2:]
            
            # Save updated history to session
            session['conversation_history'] = conversation_history

        elif any(word in command for word in ['motivation', 'quote', 'fact', 'joke']):
            category = next(word for word in ['motivation', 'quote', 'fact', 'joke'] if word in command)
            content = get_random_content(category)
            response['response'] = content
            speak_text(content)

        elif any(word in command for word in ['play', 'song', 'music']):
            success = play_music(command)
            if success:
                response['action'] = 'music'
                response['response'] = f"Playing music: {command.replace('play', '').strip()}"
            else:
                response['response'] = "Sorry, I couldn't play that music"
            speak_text(response['response'])
        
        elif 'search' in command:
            query = command.replace('search', '').strip()
            if query:
                success = search_web(query)
                if success:
                    response['action'] = 'search'
                    response['response'] = f"Searching : {query}"
                else:
                    response['response'] = "Sorry, I couldn't perform the search"
                speak_text(response['response'])
        
        elif 'open' in command:
            success = open_website(command)
            if success:
                response['action'] = 'browser'
                response['response'] = "Opening website as requested"
            else:
                response['response'] = "Sorry, I couldn't open that website"
            speak_text(response['response'])
        
        elif 'weather' in command:
            city = command.split('in')[-1].strip() if 'in' in command else None
            if city:
                weather_info = get_weather(city)
                response['response'] = weather_info
                speak_text(weather_info)
            else:
                response['response'] = "Please specify a city for weather information."
                speak_text(response['response'])
        
        else:
            # Handle general queries with conversation history
            ai_response = get_ai_response(command, conversation_history)
            response['response'] = ai_response
            speak_text(ai_response)
            
            # Update conversation history
            conversation_history.append({"role": "user", "content": command})
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Limit history size
            if len(conversation_history) > MAX_HISTORY * 2:
                conversation_history = conversation_history[-MAX_HISTORY * 2:]
            
            # Save updated history to session
            session['conversation_history'] = conversation_history

    except Exception as e:
        print(f"Error processing command: {str(e)}")
        response['status'] = 'error'
        response['response'] = "Sorry, I encountered an error processing your request."
        speak_text(response['response'])

    return jsonify(response)

# Add route to clear conversation history
@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['conversation_history'] = []
    return jsonify({'status': 'success'})

@app.route('/clear_session', methods=['POST'])
def clear_session():
    session.pop('chat_history', None)
    return jsonify({'status': 'session cleared'})

if __name__ == '__main__':
    app.run(debug=True)