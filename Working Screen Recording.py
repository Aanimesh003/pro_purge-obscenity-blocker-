import time
import numpy as np
from classifier import Classifier
import detector
import pyautogui
import tkinter as tk
import imgcompare
import image_utils
import subprocess
import emailer
from PIL import ImageGrab
detector
root = tk.Tk()

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
        time.sleep(0.2)
        screenshot = pyautogui.screenshot('pic1.png')
        is_same = imgcompare.is_equal("pic.png", "pic1.png", tolerance=.15)
        i=i+1
    #    print("image taken")
        if (is_same==False or i==10):
            i=0
            image_utils.splitimage("pic1.png")

            a = Classifier.classify("image_1.png")
            safe_per=round(100*a["image_1.png"]['safe'],2)
            print("safe_per_1",safe_per)

            a1 = Classifier.classify("image_2.png")
            safe_per1=round(100*a1["image_2.png"]['safe'],2)
            print("safe_per_2",safe_per1)

            if safe_per < 60 or safe_per1 < 60 :
                print("Further Detection Trggered")
                l=detector.Detector.detect("pic1.png") #Keyboard inputs to Close Obscene window
                if l!=[]:
                    point=l[0]['box'][0],l[0]['box'][1]
                    pyautogui.moveTo(point)
                    pyautogui.leftClick()
                    pyautogui.hotkey('ctrl', 'f4')
                    emailer.sendmail()
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
                subprocess.run(['python', 'Working Screen Recording.py'])
                # TO ADD: SEND OBSECNITY ALERT NOTIFICATION
                # Proper Integration into a Fuction
                # Launching a Script for Overlay that is a seperate file
                
    #except:
        #print("Unable to take Sreenshot Device may be Asleep")
