import pyttsx3
import speech_recognition as sr
import sqlite3
import time
import webbrowser
from googletrans import Translator
import playsound
import datetime
import os
from colorama import init, Fore, Back, Style
import pyautogui
import random
import datetime
import wikipedia
import threading
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import winsound
import pyaudio

# Initialize colorama
init()

# Set console window size and title
os.system('mode con: cols=80 lines=30')
os.system('title Gravity Assistant')

# Define colors
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
RESET = Style.RESET_ALL
CYAN = Fore.CYAN
BLUE =Fore.BLUE
MAGENTA = Fore.LIGHTMAGENTA_EX

# Clear console window
os.system('cls')

# Print welcome message in green color
print(GREEN + "=====================================")
print(GREEN + "|                                   |")
print(GREEN + "|         Gravity Assistant         |")
print(GREEN + "|                                   |")
print(GREEN + "=====================================")
print(RESET)

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


# Define some response messages
greetings = ["Hello Sir!", "Good day sir!", "How may I assist you?", "What can I do for you?","What's up, buddy?","Good to see you!","How's it going, sir?"]
confirmation = ["Ready to assist you !","How can I help?", "What can I do for you?","What can I assist you?","how can I Assist you today?"]
farewells = ["Goodbye sir!", "Have a nice day!", "Take care!","See you later, sir!","Goodbye for now, sir!!"]
checkto =["Yes Sir!", "i am listening!", "i am here sir", "ready to assist you!"]


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

def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    return current_time

def play_sound(sound_file):
    def play():
        winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
    threading.Thread(target=play).start()

def assistance_gui():
    # Create a new window
    window = tk.Tk()
    window.title("Gravity...")

    # Load the GIF image
    gif_path = "E:\projects\GOAT 1\GOAT\Eye2on (1).gif"
    gif = Image.open(gif_path)
    gif_frames = gif.n_frames

    # Create a canvas to display the GIF
    canvas = tk.Canvas(window, width=gif.width, height=gif.height)
    canvas.pack()

    # Function to play the GIF
    def play_gif():
        while window.winfo_exists():
            # Display each frame of the GIF in order
            for frame in range(gif_frames):
                gif.seek(frame)
                photo = ImageTk.PhotoImage(gif)
                canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                window.update()
                time.sleep(0.05)

    # Start playing the GIF
    play_gif()

    # Run the GUI
    window.mainloop()


# Define a function to take a selfie using the computer's camera
def take_selfie():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()

    # Get the current highest serial number in the directory
    serial_number = 1
    while os.path.exists(f"E:\GOAT\Selfies/selfie{serial_number}.jpg"):
        serial_number += 1

    # Save the selfie with the next available serial number in a specified directory
    cv2.imwrite(f"E:\GOAT\Selfies/selfie{serial_number}.jpg", frame)



def take_screenshot():
    # Get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H-%M-%S")

    # Take a screenshot using PyAutoGUI
    screenshot = pyautogui.screenshot()

    # Save the screenshot with a file name that includes the date and time
    file_name = os.path.join("Screenshots", f"screenshot_{date_time}.png")
    screenshot.save(file_name)


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
    
    elif 'play' in prompt_en.lower():
        # Open YouTube and play music
        query = prompt_en.lower().replace('play', '').strip()
        url = f'https://www.youtube.com/results?search_query={query}'
        webbrowser.open(url)
        return "Here is some songs..."
    
    elif 'music' in prompt_en.lower():
        music_dir = 'E:\GOAT\MUSIC'
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
        return 'Playing music...'
    
    elif "take screenshot" in prompt_en.lower() or "screenshot" in prompt_en.lower():
        play_sound('E:\GOAT\Screen_Shot_tone.wav')
        take_screenshot()
        return 'screenshot taken Sir!!!'
    
    elif "open notepad" in prompt_en.lower() or "notepad" in prompt_en.lower():
        os.startfile("notepad.exe")
        play_sound('E:\GOAT\notepad.wav')
        return "Notepad is now open." 
    
    elif "open cmd" in prompt_en.lower():
        os.startfile("start cmd")
        play_sound('E:\GOAT\file.wav')
        return "Command Prompt is now open."
    
    elif "open MS" in prompt_en.lower() or "open word" in prompt_en.lower():
        os.startfile("WINWORD.exe")
        play_sound('E:\GOAT\file.wav')
        return "Microsoft Word is now open."
    
    elif "open excel" in prompt_en.lower():
        os.startfile("excel.exe")
        play_sound('E:\GOAT\file.wav')
        return "Excel is now open."
    
    elif "open file" in prompt_en.lower():
        os.startfile("explorer.exe")
        return "File Explorer is now open."

    elif 'what time is it' in prompt_en.lower() or 'what time' in prompt_en.lower() or 'time' in prompt_en.lower():
        # Get current time
        current_time = get_current_time()
        return f"The current time is {current_time}"
    
        
    elif 'write essay on' in prompt_en.lower():
        # Extract the topic from the prompt
        topic = prompt_en.lower().replace('write essay on', '').strip()

        # Create a directory for saving the essays, if it does not already exist
        if not os.path.exists("essays"):
            os.mkdir("essays")

        try:
            # Fetch a summary of the topic from Wikipedia
            summary = wikipedia.summary(topic)
            # Generate an essay by combining the summary with additional text
            essay = f"An essay on {topic}:\n\n{summary}\n\nThis is an essay about {topic}."
            # Write the essay to a new text file in the "essays" directory
            with open(f"essays/{topic}.txt", "w") as f:
                f.write(essay)
            # Open the text file in Notepad
            os.system(f"notepad.exe essays/{topic}.txt")
            return None
        except wikipedia.exceptions.DisambiguationError as e:
            # If there are multiple possible Wikipedia pages for the topic, ask the user to clarify
            speak_text("Please clarify the topic.")
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                audio = recognizer.listen(source)
                try:
                    topic = translate_hindi_to_english(recognizer.recognize_google(audio))
                    summary = wikipedia.summary(topic)
                    essay = f"An essay on {topic}:\n\n{summary}\n\nThis is an essay about {topic}."
                    # Write the essay to a new text file in the "essays" directory
                    with open(f"essays/{topic}.txt", "w") as f:
                        f.write(essay)
                    # Open the text file in Notepad
                    os.system(f"notepad.exe essays/{topic}.txt")
                    return None
                except:
                    speak_text("Sorry, I could not understand the topic.")
                    return None
        except:
            speak_text("Sorry, I could not find information on the topic.")
            return None
    
    elif 'maximize' in prompt_en.lower() or 'maximise' in prompt_en.lower():
        # Maximize the current window
        pyautogui.hotkey('winleft', 'up')
        return "Maximizing the window..."
    
    elif 'minimize' in prompt_en.lower() or 'minimise' in prompt_en.lower():
        # Minimize the current window
        pyautogui.hotkey('winleft', 'down')
        return "Minimizing the window..."
    
    elif 'close window' in prompt_en.lower() or 'close' in prompt_en.lower():
        # Close all open windows
        pyautogui.hotkey('altleft', 'f4')
        return "Closing all windows..."
    
    elif 'clean memory' in prompt_en.lower():
        # Clear temporary memory
        play_sound('E:\GOAT\clenn memory.wav')
        os.system('del /q/f/s %TEMP%\*')
        return "Temporary memory cleaned successfully!"
    
    elif 'clean console' in prompt_en.lower():
        # Clear the command prompt screen
        os.system('cls')
        return "Assistance console cleared successfully!"

    elif 'restart os' in prompt_en.lower() or 'restart' in prompt_en.lower():
        # Restart the system
        os.system('shutdown /r /t 1')
        return "Restarting the system..."

    elif "shutdown" in prompt_en.lower():
        os.system("shutdown /s /t 1")
        return "Shutting down the computer now."
    
    elif 'copy' in prompt_en.lower():
        # Copy selected text
        pyautogui.hotkey('ctrl', 'c')
        return "Selected copied to!"

    elif 'cut' in prompt_en.lower():
        # Cut selected text
        pyautogui.hotkey('ctrl', 'x')
        return "Selected text cut and copied to clipboard!"

    elif 'paste' in prompt_en.lower():
        # Paste clipboard content
        pyautogui.hotkey('ctrl', 'v')
        return "content pasted successfully!"

    elif 'select all' in prompt_en.lower():
        # Select all content
        pyautogui.hotkey('ctrl', 'a')
        return "All content selected successfully!"
    
    elif 'save' in prompt_en.lower() or 'save file' in prompt_en.lower():
        # Select all content
        pyautogui.hotkey('ctrl', 's')
        return "Saved successfully!"

    elif 'delete' in prompt_en.lower():
        # Delete selected content
        pyautogui.press('delete')
        return "Selected content deleted successfully!"
    
    elif any(word in prompt_en.lower() for word in ['what', 'where', 'how', 'who','tell','tell me','which']):
        # Search for information on Wikipedia
        query = prompt_en.lower()
        result = wikipedia.summary(query, sentences=2)
        return result
    
    elif 'create folder' in prompt_en.lower():
        # Create a new folder
        pyautogui.hotkey('ctrl', 'shift', 'n')
        return "New folder created successfully!"
    
    # Add the new conditions to the existing code
    elif "take selfie" in prompt_en.lower() or "selfie" in prompt_en.lower():
        take_selfie()
        return 'Selfie taken, Sir!'
    



    # If no matching question was found, add the new question and its response to the database
    else:
        print(RED + "Please provide a response to this question or say 'no' to skip:" + Style.RESET_ALL)
        speak_text("Please provide a response to this question or say 'no' to skip:")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                response_text = translate_hindi_to_english(recognizer.recognize_google(audio))
            except:
                response_text = ""
         #if the user say the no so the response has been clear.       
        if response_text.lower() == "no" or response_text.strip() == "":
            print(MAGENTA + "I Clear The Response....."+Style.RESET_ALL)
            play_sound('E:\GOAT\clear the response.wav')
            speak_text("I clear the response!")
            print(GREEN + "Listening....."+Style.RESET_ALL)
            return None
        elif response_text == "":
            print(MAGENTA + "No response given. Clearing the response in 5 seconds." + Style.RESET_ALL)
            speak_text("No response given. Clearing the response in 5 seconds.")
            time.sleep(5)
            play_sound('E:\projects\GOAT 1\GOAT\listen2.wav')
            return 'Listening......'
        else:
            # Add prompt and response to the database
            add_response(prompt_en.lower(), response_text)
            return response_text

# Speak text using the text-to-speech engine
def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    listening = False
    while True:
        if not listening:
            # Wait for user to say "Gravity"
            print(MAGENTA + "Say 'Gravity' to wake up the assistant..."+Style.RESET_ALL)
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                audio = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio)
                    if transcription.lower() == "gravity":
                        print("")
                        print(GREEN + "Connecting...."+ Style.RESET_ALL)
                        print("")
                        # Play a song when the assistant wakes up
                        play_sound("E:\projects\GOAT 1\GOAT\song1.wav")
                        threading.Thread(target=assistance_gui).start()
                        speak_text("Importing All The Preferences!")
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>")
                        speak_text("System is now fully Operational")
                       # Greet the user with good morning or good evening
                        hour = datetime.datetime.now().hour
                        if 6 <= hour < 12:
                            print(YELLOW + "Hello, Good morning Sir!" + Style.RESET_ALL)
                            speak_text("Hello, Good morning Sir!")
                        elif 12 <= hour < 18:
                            print(YELLOW + "Hello, Good afternoon Sir!" + Style.RESET_ALL)
                            speak_text("Hello, Good afternoon Sir!")
                        else:
                            print(YELLOW + "Hello, Good evening Sir!" + Style.RESET_ALL)
                            speak_text("Hello, Good evening Sir!")
                        
                        # Introduce the assistant
                        print(RED + "......................." + Style.RESET_ALL)
                        speak_text(random.choice(confirmation))
                        play_sound('E:\projects\GOAT 1\GOAT\listen2.wav')
                        print(GREEN + "Listening....!" + Style.RESET_ALL)
                        
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
                    print(BLUE + f"You said: {transcription}" + Style.RESET_ALL)
                    if transcription.lower() == "goodbye" or transcription.lower() == "stop listening":
                        print(CYAN + "Goodbye!" + Style.RESET_ALL)
                        speak_text(random.choice(farewells))
                        play_sound('E:\GOAT\song2.wav')
                        listening = False
                        end_time = time.time()
                        if end_time - start_time > 120:
                            print(GREEN + "Assistant is going to sleep..." + Style.RESET_ALL)
                            speak_text("Assistant is going to sleep...")
                            time.sleep(2)
                            play_sound('E:\GOAT\shut20.wav')
                    #introduction of Gravity
                    elif transcription.lower() == "gravity":
                        speak_text(random.choice(checkto))
                    
                    else:
                        # Generate response
                        response = generate_response(transcription)
                        if response:
                            print(GREEN + f"AI Says: {response}" + Style.RESET_ALL)
                            speak_text(response)
                        
                except:
                    pass

if __name__ == "__main__":
    main()