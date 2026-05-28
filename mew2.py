import pyttsx3
import speech_recognition as sr
import sqlite3
import random
import time
import webbrowser
from googletrans import Translator

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the voice language to English
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Connect to the SQLite3 database
conn = sqlite3.connect('responses.db')
c = conn.cursor()

# Create the responses table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS responses
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              question TEXT,
              response TEXT)''')

# Load responses from the database
def get_responses():
    responses = {}
    for row in c.execute('SELECT question, response FROM responses'):
        responses[row[0]] = row[1]
    return responses

# Add a new response to the database
def add_response(question, response):
    c.execute('INSERT INTO responses (question, response) VALUES (?, ?)', (question, response))
    conn.commit()

# Translate text from Hindi to English
def translate_hindi_to_english(text):
    translator = Translator()
    return translator.translate(text, src='hi', dest='en').text

# Generate a response based on the input prompt
def generate_response(prompt):
    # Load responses from the database
    responses = get_responses()
    
    # Translate prompt to English
    prompt_en = translate_hindi_to_english(prompt)

    # Check if the prompt matches a question in the database
    if prompt_en.lower() in [q.lower() for q in responses.keys()]:
        response_en = responses[prompt_en.lower()]
        return response_en

    # Check for specific keywords in the prompt
    if 'search' in prompt_en.lower():
        # Open Chrome and search for information
        query = prompt_en.lower().replace('search', '').strip()
        url = f'https://www.google.com/search?q={query}'
        webbrowser.open(url)
        return "Here are some results..."

    # If no matching question was found, add the new question and its response to the database
    else:
        speak_text("Please provide a response to this question or say 'clear' to skip:")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                response_text = translate_hindi_to_english(recognizer.recognize_google(audio))
            except:
                response_text = ""
        if response_text.lower() == "clear":
            speak_text("I clear the response!")
            print("Listening.....")
            return None
        else:
            # Add prompt and response to the database
            add_response(prompt_en.lower(), response_text)
            return response_text

def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    listening = False
    while True:
        if not listening:
            # Wait for user to say "Gravity"
            print("Say 'Gravity' to wake up the assistant...")
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                audio = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio)
                    if transcription.lower() == "gravity":
                        print("Assistant is awake.")
                        speak_text("How can I assist you?")
                        listening = True
                        start_time = time.time()
                except:
                    pass
        else:
            # Listen for user input
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                audio = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio)
                    print(f"You said: {transcription}")
                    if transcription.lower() == "goodbye":
                        speak_text("Goodbye!")
                        listening = False
                        end_time = time.time()
                        if end_time - start_time > 120:
                            print("Assistant is going to sleep...")
                            speak_text("Assistant is going to sleep...")
                            time.sleep(2)
                    else:
                        # Generate response
                        response = generate_response(transcription)
                        if response:
                            print(f"AI Says: {response}")
                            speak_text(response)
                except:
                    pass

if __name__ == "__main__":
    main()
