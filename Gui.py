import tkinter as tk
import subprocess
import threading
class DeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python DeskApp")

        self.start_button = tk.Button(root, text="Start", command=self.show_detect_buttons)
        self.detect_video_button = tk.Button(root, text="Detect Video", command=self.detect_video)
        self.detect_audio_button = tk.Button(root, text="Detect Audio", command=self.detect_audio)
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
        while self.recording:
            subprocess.run(['python', 'Working Screen Recording.py'])
            

    def run_audio_detection(self):
        self.audio_detecting = True
        while self.audio_detecting:
            subprocess.run(['python', 'beeping_obscenity.py'])
            

    def stop_processes(self):
        self.recording = False
        self.audio_detecting = False
        if self.video_thread:
            self.video_thread.join()  # Wait for the video thread to finish
        if self.audio_thread:
            self.audio_thread.join()  # Wait for the audio thread to finish

# Create the main window
root = tk.Tk()
root.title("Button Example")

app = DeskApp(root)

# Create the Start button
app.start_button.pack(pady=20)

# Run the main event loop
root.mainloop()
