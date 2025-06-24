# Parker AI Assistant: Personalized Assistant for Responsive Knowledge Research and Execution

Parker is a sophisticated AI-powered virtual assistant designed to provide responsive knowledge research and execution capabilities. Built using Python, Flask, and modern web technologies, Parker offers a seamless interaction experience through both voice and a modern web interface.

## Core Features

### Voice Interaction

- Advanced speech recognition for hands-free operation
- Text-to-speech synthesis with customizable voice settings
- Real-time voice input visualization
- Support for continuous conversation

### AI Capabilities

- Powered by Groq's LLaMA 3.3 70B model
- Contextual conversation memory (stores up to 5 previous exchanges)
- Natural language understanding and processing
- Personalized responses with conversation history tracking

### Utility Features

- **Weather Information**: Real-time weather data for any city
- **Web Integration**:
  - Smart web search functionality
  - Website navigation commands
  - Music playback support (YouTube Music, Spotify, SoundCloud)
- **Entertainment**:
  - Random facts generator
  - Programming jokes
  - Motivational quotes
  - Daily facts
- **Time & Date**: Real-time information with natural language processing

### Web Interface

- Modern, responsive design
- Dark/Light theme toggle
- Voice visualization effects
- Quick access feature buttons
- Command suggestions
- Chat history display
- Voice settings panel with customizable options

### Technical Highlights

- **API Integrations**:
  - Groq AI for natural language processing
  - OpenWeatherMap for weather data
  - Various APIs for random content generation
- **Voice Processing**:
  - pyttsx3 for text-to-speech
  - speech_recognition for voice input
- **Web Framework**:
  - Flask-based backend
  - Session management for conversation history
  - Asynchronous command processing
- **Security**:
  - API key protection
  - Session-based conversation management
  - Error handling and input validation

## User Interface Features

- Clean, intuitive design
- Real-time response indicators
- Voice activity visualization
- Easy-to-use command input
- Conversation history display
- Quick action buttons

## Keyboard Shortcuts

- `Ctrl + Shift + V`: Toggle voice input
- `Ctrl + /`: Focus text input
- `Esc`: Clear input field

## System Requirements

- Python 3.7+
- Internet connection for API services
- Microphone for voice input
- Speakers for voice output

## Setup Instructions

1. Create virtual environment:

   ```bash
   python -m venv jarvis_env
   ```

2. Activate virtual environment:

   ```bash
   # Windows
   jarvis_env\Scripts\activate

   # Unix/MacOS
   source jarvis_env/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file with your API keys:

   ```
   GROQ_API_KEY=your_groq_api_key
   WEATHER_API_KEY=your_weather_api_key
   ```

## Running the Application

To run the Parker AI Assistant, follow these steps:

1.  **Activate your Python virtual environment:**

    ```powershell
    .\jarvis_env\Scripts\activate
    ```

2.  **Navigate to the web application directory:**

    ```powershell
    cd parker_web
    ```

3.  **Start the Flask web server:**

    ```powershell
    python app.py
    ```

    This will start the web server, typically accessible at `http://127.0.0.1:5000`. You will see output similar to this:

    ```

    ```

- Serving Flask app 'app'
- Debug mode: on
  WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
- Running on http://127.0.0.1:5000
  Press CTRL+C to quit
- Restarting with stat
- Debugger is active!


1.  **Open your web browser** and go to `http://127.0.0.1:5000` to access the web interface.

_Note: The `final.py` file contains the core backend logic used by the web application. Running `python final.py` directly might execute some of the backend scripts but does not start the web server or provide the full interactive experience._

Created by Jayanth
