import time
import numpy as np
from nudenet import NudeClassifier
import pyautogui
import tkinter as tk
import imgcompare


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
i=0
while True:
    #Optimization Required Need Faster Screenshot Implementation
    screenshot = pyautogui.screenshot('pic.png')
    screenshot = pyautogui.screenshot('pic1.png')
    is_same = imgcompare.is_equal("pic.png", "pic1.png", tolerance=2.5)
    i=i+1
    print(i)
#    print("image taken")
    if (is_same==False or i==10):
        i=0
        a = classifier.classify("pic.png")

        safe_per=round(100*a["pic.png"]['safe'],2)      
    
        if safe_per < 40 :
            pyautogui.hotkey('alt', 'f4') #Keyboard inputs to Close Obscene window
            # TO ADD: SEND OBSECNITY ALERT NOTIFICATION
            # Proper Integration into a Fuction
            # Launching a Script for Overlay that is a seperate file
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
        time.sleep(0.3)
