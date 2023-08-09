import time
from nudenet import NudeDetector
import pyautogui
import tkinter as tk
detector = NudeDetector()

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

i=0
while True:
    #try:
        #Optimization Required Need Faster Screenshot Implementation
        screenshot = pyautogui.screenshot('pic.png')
        print("image captured")
        l=detector.detect("pic.png") 
        print("passed through model")
        time.sleep(.2)
        if len(l)>0:

            point=l[0]['box'][0],l[0]['box'][1]
            pyautogui.moveTo(point)
            pyautogui.leftClick()
            pyautogui.hotkey('alt', 'f4')
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
    #except:
    #    print("Unable to take Sreenshot Device may be Asleep")
