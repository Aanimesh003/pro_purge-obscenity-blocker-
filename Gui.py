import tkinter as tk
import subprocess
import threading

class DeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python DeskApp")

        self.login_frame = None  # Initialize login_frame

        # Create and place widgets for the login frame
        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        login_label = tk.Label(self.login_frame, text="Login", font=("Helvetica", 16, "bold"))
        login_label.pack(pady=20)

        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.username_entry.insert(0, "Username:")  # Placeholder
        self.username_entry.bind("<FocusIn>", self.clear_placeholder)
        self.username_entry.bind("<Return>", lambda event: self.authenticate())
        self.username_entry.pack(pady=10)

        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 12))
        self.password_entry.insert(0, "Password:")  # Placeholder
        self.password_entry.bind("<FocusIn>", self.clear_placeholder)
        self.password_entry.bind("<Return>", lambda event: self.authenticate())
        self.password_entry.pack(pady=10)

        login_button = tk.Button(self.login_frame, text="Login", command=self.authenticate, font=("Helvetica", 12))
        login_button.pack(pady=20)

        self.auth_status = tk.Label(self.login_frame, text="", font=("Helvetica", 12))
        self.auth_status.pack()

    def clear_placeholder(self, event):
        if event.widget.get() in ["Username:", "Password:"]:
            event.widget.delete(0, tk.END)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "user" and password == "123":
            self.show_main_screen()
        else:
            self.auth_status.config(text="Invalid credentials", fg="red")

    def show_main_screen(self):
        if self.login_frame:
            self.login_frame.destroy()

        self.title_label = tk.Label(self.root, text="Welcome to DeskApp", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        self.detect_video_button = tk.Button(self.root, text="Detect Video", command=self.detect_video, bg="green", font=("Helvetica", 12))
        self.detect_audio_button = tk.Button(self.root, text="Detect Audio", command=self.detect_audio, bg="green", font=("Helvetica", 12))
        self.detect_text_button = tk.Button(self.root, text="Detect Text", command=self.detect_text, bg="green", font=("Helvetica", 12))
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_processes, bg="gray", font=("Helvetica", 12), state=tk.DISABLED)

        self.detect_video_button.pack(pady=10)
        self.detect_audio_button.pack(pady=10)
        self.detect_text_button.pack(pady=10)
        self.stop_button.pack(pady=10)

        self.recording = True
        self.audio_detecting = True
        self.text_detecting = True
        self.video_thread = threading.Thread(target=self.run_video_detection)
        self.audio_thread = threading.Thread(target=self.run_audio_detection)
        self.text_thread = threading.Thread(target=self.run_audio_detection)
        self.video_thread.start()
        self.audio_thread.start()
        self.audio_thread.start()

    def detect_video(self):
        self.detect_video_button.config(state=tk.DISABLED)
        self.detect_audio_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def detect_audio(self):
        self.detect_video_button.config(state=tk.DISABLED)
        self.detect_audio_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def detect_text(self):
        self.detect_text_button.config(state=tk.DISABLED)
        self.detect_text_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def run_video_detection(self):
        self.detect_video_button.config(bg="green")  
        while self.recording:
            subprocess.run(['python', 'Working Screen Recording.py'])
            print("Detecting video...")

    def run_audio_detection(self):
        self.detect_audio_button.config(bg="green")  
        while self.audio_detecting:
            subprocess.run(['python', 'beeping_obscenity.py'])
            print("Detecting audio...")

    def run_text_detection(self):
        self.detect_text_button.config(bg="green")  
        while self.recording:
            subprocess.run(['python', 'text_profanity.py'])
            print("Detecting text...")

    def stop_processes(self):
        self.recording = False
        self.audio_detecting = False
        self.text_detecting = False
        if self.video_thread:
            self.video_thread.join()  
            self.detect_video_button.config(state=tk.NORMAL, bg="red")
        if self.audio_thread:
            self.audio_thread.join()  
            self.detect_audio_button.config(state=tk.NORMAL, bg="red")
        if self.text_thread:
            self.text_thread.join()
            self.detect_text_button.config(state=tk.NORMAL, bg="red")
        self.detect_video_button.config(state=tk.NORMAL)
        self.detect_audio_button.config(state=tk.NORMAL)
        self.detect_text_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("DeskApp Login")

app = DeskApp(root)

# Set window size
window_width = 400
window_height = 300
root.geometry(f"{window_width}x{window_height}")

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"+{x}+{y}")

# Run the main event loop
root.mainloop()
