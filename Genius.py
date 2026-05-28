import pyttsx3
import speech_recognition as sr
import json
import time
import webbrowser
import datetime
import pyautogui
import os
from googletrans import Translator


# Initialize the text-to-speech engine
engine = pyttsx3.init()


# Set the voice language to English
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Load responses from JSON file
with open('responses.json', 'r') as f:
    responses = json.load(f)

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error")


def translate_hindi_to_english(text):
    translator = Translator()
    return translator.translate(text, src='hi', dest='en').text


def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    return current_time

def generate_response(prompt):
    # Load JSON file
    with open('responses.json', 'r') as f:
        data = json.load(f)

    # Translate prompt to English
    prompt_en = translate_hindi_to_english(prompt)

    # Check if the prompt matches a question in the JSON file
    for question in data.keys():
        if prompt_en.lower() in translate_hindi_to_english(question).lower():
            response_en = translate_hindi_to_english(data[question])
            return response_en

    # Check for specific keywords in the prompt
    if 'search' in prompt_en.lower():
        # Open Chrome and search for information
        query = prompt_en.lower().replace('search', '').strip()
        url = f'https://www.google.com/search?q={query}'
        webbrowser.open(url)
        return "Here is Some Results..."

    elif 'play' in prompt_en.lower() and 'youtube' in prompt_en.lower():
        # Open YouTube and play music
        query = prompt_en.lower().replace('play', '').replace('youtube', '').strip()
        url = f'https://www.youtube.com/results?search_query={query}'
        webbrowser.open(url)
        return "Playing songs on YouTube..."
    
    elif 'what time is it' in prompt_en.lower():
        # Get current time
        current_time = get_current_time()
        return f"The current time is {current_time}"

    elif 'maximize' in prompt_en.lower():
        # Maximize the current window
        pyautogui.hotkey('winleft', 'up')
        return "Maximizing the window..."
    
    elif 'close window' in prompt_en.lower():
        # Close all open windows
        pyautogui.hotkey('altleft', 'f4')
        return "Closing all windows..."
    
    elif 'close all windows' in prompt_en.lower():
        # Close all open windows
        pyautogui.hotkey('altleft', 'f4')
        return "Closing all windows..."
        

    else:
        # If no matching question was found, add the new question and its response to the JSON file
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
            # Add prompt and response to the JSON file
            data[prompt] = response_text
            with open('responses.json', 'w') as f:
                json.dump(data, f, indent=None, separators=(',', ':'))
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
