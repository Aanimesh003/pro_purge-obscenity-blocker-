import tkinter as tk

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

# List of obscene words (for demonstration purposes)
obscene_words = ["obscene", "vulgar", "inappropriate"]


def detect_text():
    detected_text = "This is an obscene text"  # Replace this with actual text detection logic

    # Clear the text panel
    text_panel.delete("1.0", tk.END)

    # Check for obscene words
    if any(word in detected_text.lower() for word in obscene_words):
        text_panel.insert("1.0", detected_text + "\n", "alert")
        alert_button.pack()
        warning_label.config(text="Warning: Detected obscene content! Please close the site.")
        warning_label.pack()
    else:
        text_panel.insert("1.0", detected_text + "\n")
        alert_button.pack_forget()
        warning_label.pack_forget()


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
start_button = tk.Button(main_frame, text="Start", command=start_action)
start_button.pack(pady=10)

stop_button = tk.Button(main_frame, text="Stop", command=stop_action)
stop_button.pack(pady=10)

text_panel = tk.Text(main_frame, height=10, width=40)
text_panel.pack(pady=10)

detect_button = tk.Button(main_frame, text="Detect Text", command=detect_text)
detect_button.pack(pady=5)

alert_button = tk.Button(main_frame, text="ALERT", bg="white", fg="red")
alert_button.pack_forget()

warning_label = tk.Label(main_frame, text="", fg="red")
warning_label.pack_forget()


# Hide the main frame initially
main_frame.pack_forget()

# Run the main event loop
root.mainloop()
