import tkinter as tk
import subprocess
import threading
from tkinter import ttk

class DeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python DeskApp")

        self.detect_video_button = tk.Button(root, text="Detect Video", command=self.detect_video, bg="red")
        self.detect_audio_button = tk.Button(root, text="Detect Audio", command=self.detect_audio, bg="red")
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_processes)

        self.recording = False
        self.audio_detecting = False
        self.video_thread = None
        self.audio_thread = None

    def show_detect_buttons(self):
        self.start_button.pack_forget()
        self.detect_video_button.pack(pady=5)
        self.detect_audio_button.pack(pady=5)
        self.stop_button.pack(pady=5)

    def detect_video(self):
        self.video_thread = threading.Thread(target=self.run_video_detection)
        self.video_thread.start()

    def detect_audio(self):
        self.audio_thread = threading.Thread(target=self.run_audio_detection)
        self.audio_thread.start()

    def run_video_detection(self):
        self.recording = True
        self.detect_video_button.config(bg="green")  # Change button color to green
        while self.recording:
            subprocess.run(['python', 'Working Screen Recording.py'])
            print("Detecting video...")

    def run_audio_detection(self):
        self.audio_detecting = True
        self.detect_audio_button.config(bg="green")  # Change button color to green
        while self.audio_detecting:
            subprocess.run(['python', 'beeping_obscenity.py'])
            print("Detecting audio...")

    def stop_processes(self):
        self.recording = False
        self.audio_detecting = False
        if self.video_thread:
            self.video_thread.join()  # Wait for the video thread to finish
            self.detect_video_button.config(bg="red")  # Change button color back to red
        if self.audio_thread:
            self.audio_thread.join()  # Wait for the audio thread to finish
            self.detect_audio_button.config(bg="red")  # Change button color back to red

# Create the main window
style = ttk.Style()
style.theme_use("clam")
root = tk.Tk()
root.title("Button Example")

app = DeskApp(root)

# Center the start button
app.start_button = tk.Button(root, text="Start", command=app.show_detect_buttons, width=20, height=2)
app.start_button.pack(pady=20, padx=100)

# Increase the size of the GUI window
root.geometry("400x300")  # Adjust the width and height as needed

# Run the main event loop
root.mainloop()
