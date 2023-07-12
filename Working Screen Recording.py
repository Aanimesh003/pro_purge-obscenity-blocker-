import time
import numpy as np
from nudenet import NudeClassifier
import pyautogui

classifier = NudeClassifier()
frame_rate = 30
interval = 1 / frame_rate

while True:
    screenshot = pyautogui.screenshot('pic.png')
    
    a = classifier.classify("pic.png")
    
    time.sleep(interval)
    
    unsafe_per=round(100*a["pic.png"]['unsafe'],2)
    safe_per=round(100*a["pic.png"]['safe'],2)          
    print("Unsafe",unsafe_per,"%")
    print("Safe",safe_per,"%")
                
