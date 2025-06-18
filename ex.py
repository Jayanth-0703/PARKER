from groq import Groq

# Initialize Groq client
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def get_ai_response(prompt):
    """Get AI response using Groq API"""
    try:
        chat_completion = client.chat.completions.create(
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
            model="llama-3.3-70b-versatile",  # Updated to use available model
            stream=False,
            temperature=0.7,
            max_tokens=500
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return "Sorry, I'm having trouble accessing my knowledge right now."

# Test the functionality
if __name__ == "__main__":
    while True:
        user_input = input("\nAsk me anything (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        response = get_ai_response(user_input)
        print(f"\nJarvis: {response}")