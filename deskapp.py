import tkinter as tk
import time
import numpy as np
from nudenet import NudeClassifier
import pyautogui
import speechmatics
from httpx import HTTPStatusError
import asyncio
import pyaudio
import winsound



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
            def close_overlay(overlay, freeze_screen):
                overlay.grab_release()
                overlay.destroy()
                freeze_screen.destroy()
                root.quit()  # Exit the application after the overlay is closed

            def show_overlay():
                overlay = tk.Toplevel(root)
                overlay.attributes('-fullscreen', True)
                overlay.attributes('-topmost', True)  # Keep the overlay window on top of other windows
                overlay.grab_set_global()  # Grab all events to the overlay window

                overlay.configure(bg='red')  # Set the background color to red

                # Disable events on the overlay window to restrict interaction
                overlay.grab_set()

                message_label = tk.Label(overlay, text="UNSAFE CONTENT DETECTED!", font=('Arial', 60, 'bold'), fg='white', bg='red')
                message_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                # After 20 seconds, close the overlay and the application
                overlay.after(2000, close_overlay, overlay, freeze_screen)

            classifier = NudeClassifier()

            while True:
                #Optimization Required Need Faster Screenshot Implementation
                screenshot = pyautogui.screenshot('pic.png')
                
                a = classifier.classify("pic.png")

                safe_per=round(100*a["pic.png"]['safe'],2)      
            
                if safe_per < 40 :
                    pyautogui.hotkey('alt', 'f4')
                    # TO ADD: SEND OBSECNITY ALERT NOTIFICATION
                    # Proper Integration into a Fuction
                    # Launching a Script for Overlay that is a seperate file
                    # Integraing Keyboard inputs to Close Obscene window
                    root = tk.Tk()
                    root.attributes('-fullscreen', True)
                    root.withdraw()  # Hide the root window

                    # Create a transparent window to freeze the screen
                    freeze_screen = tk.Toplevel(root)
                    freeze_screen.attributes('-fullscreen', True)
                    freeze_screen.attributes('-alpha', 0)  # Make the window transparent
                    freeze_screen.attributes('-topmost', True)  # Keep the transparent window on top of other windows
                    freeze_screen.grab_set_global()  # Grab all events to the transparent window

                    # Show the overlay after a short delay
                    root.after(100, show_overlay)
                    root.mainloop()

                        
                print("safe",safe_per,"%")

        def detect_audio(self):
            if not self.audio_detecting:
                self.audio_detecting = True
                audio_thread = threading.Thread(target=self.detect_audio_thread)
                audio_thread.start()

        def detect_audio_thread(self):
            API_KEY = "pK4jrLchh4YCBrK2aKrJymAlqtdIU6BW"
            LANGUAGE = "en"
            CONNECTION_URL = f"wss://eu2.rt.speechmatics.com/v2/{LANGUAGE}"
            DEVICE_INDEX = -1
            CHUNK_SIZE = 5120


            class AudioProcessor:
                def __init__(self):
                    self.wave_data = bytearray()
                    self.read_offset = 0

                async def read(self, chunk_size):
                    while self.read_offset + chunk_size > len(self.wave_data):
                        await asyncio.sleep(0.001)
                    new_offset = self.read_offset + chunk_size
                    data = self.wave_data[self.read_offset:new_offset]
                    self.read_offset = new_offset
                    return data

                def write_audio(self, data):
                    self.wave_data.extend(data)
                    return


            audio_processor = AudioProcessor()


            def stream_callback(in_data, frame_count, time_info, status):
                audio_processor.write_audio(in_data)
                return in_data, pyaudio.paContinue



            p = pyaudio.PyAudio()
            if DEVICE_INDEX == -1:
                DEVICE_INDEX = p.get_default_input_device_info()['index']
                device_name = p.get_default_input_device_info()['name']
                DEF_SAMPLE_RATE = int(p.get_device_info_by_index(DEVICE_INDEX)['defaultSampleRate'])
                device_seen = set()
                for i in range(p.get_device_count()):
                    if p.get_device_info_by_index(i)['name'] not in device_seen:
                        device_seen.add(p.get_device_info_by_index(i)['name'])
                        try:
                            supports_input = p.is_format_supported(DEF_SAMPLE_RATE, input_device=i, input_channels=1, input_format=pyaudio.paFloat32)
                        except Exception:
                            supports_input = False
                        if supports_input:
                            print(f"-- To use << {p.get_device_info_by_index(i)['name']} >>, set DEVICE_INDEX to {i}")
                print("***\n")

            SAMPLE_RATE = int(p.get_device_info_by_index(DEVICE_INDEX)['defaultSampleRate'])
            device_name = p.get_device_info_by_index(DEVICE_INDEX)['name']

            print(f"\nUsing << {device_name} >> which is DEVICE_INDEX {DEVICE_INDEX}")

            stream = p.open(format=pyaudio.paFloat32,
                            channels=1,
                            rate=SAMPLE_RATE,
                            input=True,
                            frames_per_buffer=CHUNK_SIZE,
                            input_device_index=DEVICE_INDEX,
                            stream_callback=stream_callback
            )



            conn = speechmatics.models.ConnectionSettings(
                url=CONNECTION_URL,
                auth_token=API_KEY,
                generate_temp_token=True,
            )



            ws = speechmatics.client.WebsocketClient(conn)



            conf = speechmatics.models.TranscriptionConfig(
                language=LANGUAGE,
                enable_partials=True,
                max_delay=2,
            )



            OBSCENE_WORDS = ['ass', 'shit', 'dick', 'fuck', 'pussy', 'asshole', 'bastard', 'bitch', 'cunt', 'dick head']

            def detect_obscene_words(transcript):
                detected_obscene_words = [word for word in OBSCENE_WORDS if word in transcript.lower()]
                return detected_obscene_words




            def save_transcript_to_file(transcript, file_path):
                with open(file_path, 'a') as file:
                    file.write(transcript + '\n')


            def save_temp_words_to_file(transcript, file_path):
                with open(file_path, 'a') as file:
                    file.write(transcript + '\n')
                


            global trsn,li,trsn2
            trsn=""
            trsn2=""
            li=0
            def print_partial_transcript(msg):
                transcript=msg['metadata']['transcript']
                print(f"[partial] {msg['metadata']['transcript']}")

                transcript = transcript.lower()
                global trsn,li,trsn2
                if li==0:
                    trsn=transcript
                    li=1

                trsn2=transcript
                if li!=0:
                    if trsn in transcript:
                        transcript = transcript.replace(trsn,"")
                    trsn=trsn2
                print(transcript)

                detected_obscene_words = detect_obscene_words(transcript)
                if detected_obscene_words:
                    with open('temp.txt', 'r') as file:
                        content = file.read()
                    words_in_file = content.split()
                    for word in words_in_file:
                        if word in detected_obscene_words:
                            return
                        else:
                            beep_sound_for_1_second()
                            return
                        

                    print(f"Detected obscene words: {', '.join(detected_obscene_words)}")



            def print_transcript(msg):
                transcript=msg['metadata']['transcript']

                global trsn,li,trsn2
                transcript=transcript.lower()
                if trsn in transcript:
                    transcript = transcript.replace(trsn,"")
                

                li=0
                trsn=""
                trsn2=""



            def beep_sound_for_1_second():
                winsound.Beep(3500,1000)



            ws.add_event_handler(
                event_name=speechmatics.models.ServerMessageType.AddPartialTranscript,
                event_handler=print_partial_transcript,
            )



            ws.add_event_handler(
                event_name=speechmatics.models.ServerMessageType.AddTranscript,
                event_handler=print_transcript,
            )



            settings = speechmatics.models.AudioSettings()
            settings.encoding = "pcm_f32le"
            settings.sample_rate = SAMPLE_RATE
            settings.chunk_size = CHUNK_SIZE

            print("Starting transcription (type Ctrl-C to stop):")
            try:
                ws.run_synchronously(audio_processor, conf, settings)
            except KeyboardInterrupt:
                print("\nTranscription stopped.")
            except HTTPStatusError as e:
                if e.response.status_code == 401:
                    print('Invalid API key - Check your API_KEY at the top of the code!')
                else:
                    raise e



# Hide the main frame initially
main_frame.pack_forget()

# Run the main event loop
def main():
    root = tk.Tk()
    app = DeskApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
