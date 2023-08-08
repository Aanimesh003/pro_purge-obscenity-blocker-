import tkinter as tk
import subprocess



def login():
    username = entry_username.get()
    password = entry_password.get()

    # Add your authentication logic here
    # For example, you could check the username and password against a database or hardcoded values
    if username == "user" and password == "123":
        message_label.config(text="Login successful!")
        show_main_page()
    else:
        message_label.config(text="Invalid username or password")

def show_main_page():
    login_frame.pack_forget()  # Hide the login frame
    main_frame.pack(pady=20)   # Show the main frame
    start_button.pack()  # Show the "Start" button
    stop_button.pack()   # Show the "Stop" button

def start_action():
    message_label.config(text="Start button clicked")

def stop_action():
    message_label.config(text="Stop button clicked")
# Create the main window
root = tk.Tk()
root.title("Login Page")

# Create the frames
login_frame = tk.Frame(root)
login_frame.pack(pady=20)

main_frame = tk.Frame(root)

# Widgets for the login frame
label_username = tk.Label(login_frame, text="Username:")
label_username.pack(pady=5)
entry_username = tk.Entry(login_frame)
entry_username.pack(pady=5)

label_password = tk.Label(login_frame, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(login_frame, show="*")
entry_password.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack(pady=10)

message_label = tk.Label(login_frame, text="")
message_label.pack(pady=5)

# Widgets for the main frame
class DeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python DeskApp")

        self.start_button = tk.Button(root, text="Start", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop", state=tk.DISABLED, command=self.stop_recording)
        self.stop_button.pack()


        self.audio_button = tk.Button(root, text="Detect Audio", command=self.detect_audio)
        self.audio_button.pack()

        self.recording = False
        self.audio_detecting = False
    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        recording_thread = threading.Thread(target=self.record_screen)
        recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def record_screen(self):
            

        
            
            
        subprocess.run(['python', 'Working Screeb Recording.py'])
            

    def detect_audio(self):
        if not self.audio_detecting:
            self.audio_detecting = True
            audio_thread = threading.Thread(target=self.detect_audio_thread)
            audio_thread.start()

    def detect_audio_thread(self):
            
             

            
        subprocess.run(['python', 'beeping_obscenity.py'])
            



# Hide the main frame initially
main_frame.pack_forget()

# Run the main event loop
def main():
    root = tk.Tk()
    app = DeskApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()