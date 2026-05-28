import tkinter as tk
from PIL import Image, ImageTk
import threading
import queue
import time
from os import assistant 



class App:
    def __init__(self, master):
        self.master = master
        self.assistants = assistant.Assistant()

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.voice_frames = [ImageTk.PhotoImage(Image.open(f"voice_{i}.png")) for i in range(8)]
        self.voice_image = self.canvas.create_image(200, 200, image=self.voice_frames[0])
        self.voice_index = 0

        self.queue = queue.Queue()
        self.poll_queue()

        self.listen_button = tk.Button(master, text="Listen", command=self.start_listening)
        self.listen_button.pack()

    def poll_queue(self):
        try:
            response = self.queue.get(0)
            self.display_response(response)
        except queue.Empty:
            pass
        self.master.after(100, self.poll_queue)

    def start_listening(self):
        self.listen_button.config(state=tk.DISABLED)
        self.canvas.itemconfig(self.voice_image, image=self.voice_frames[0])
        self.assistant.start_listening(self.queue, self.show_voice_animation)

    def show_voice_animation(self, stop):
        while not stop.is_set():
            self.voice_index = (self.voice_index + 1) % len(self.voice_frames)
            self.canvas.itemconfig(self.voice_image, image=self.voice_frames[self.voice_index])
            time.sleep(0.1)

    def display_response(self, response):
        self.canvas.itemconfig(self.voice_image, image=self.voice_frames[0])
        self.listen_button.config(state=tk.NORMAL)
        if response:
            response = response.capitalize()
            label = tk.Label(self.master, text=response, font=("Arial", 16))
            label.pack(pady=20)
            label.after(5000, lambda: label.destroy())

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()