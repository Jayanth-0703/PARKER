import speech_recognition as sr
import pyttsx3


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def test_mic_capture():
    recognizer = sr.Recognizer()
    try:
        # List available microphones
        mics = sr.Microphone.list_microphone_names()
        print("\nAvailable Microphones:")
        for i, mic in enumerate(mics):
            print(f"{i}: {mic}")

        with sr.Microphone() as source:
            print("\n🎤 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2)

            print("🎤 Please speak something...")
            speak("Please speak something")

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("✅ Audio captured successfully!")

                try:
                    text = recognizer.recognize_google(audio)
                    print(f"\nYou said: {text}")
                    speak(f"I heard: {text}")
                    return True
                except sr.UnknownValueError:
                    print("❌ Could not understand the audio")
                    return False

            except sr.WaitTimeoutError:
                print("❌ No audio detected within timeout period")
                return False

    except Exception as e:
        print(f"❌ Error during microphone test: {str(e)}")
        return False


if __name__ == "__main__":
    print("=== Microphone Capture Test ===")
    result = test_mic_capture()
    print("\nTest Result:", "Passed ✅" if result else "Failed ❌")
