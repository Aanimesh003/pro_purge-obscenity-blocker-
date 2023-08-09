# Import module
from nudenet import NudeDetector
import pyautogui
# initialize detector (downloads the checkpoint file automatically the first time)
detector = NudeDetector() # detector = NudeDetector('base') for the "base" version of detector.

# Detect single image
l=detector.detect("C:\\Users\\ryana\\OneDrive\\Documents\\Amity\\Competition\\Screenshot.png")
# fast mode is ~3x faster compared to default mode with slightly lower accuracy.
#l=detector.detect("C:\\Users\\ryana\\OneDrive\\Documents\\Amity\\Competition\\Screenshot.png", mode='fast')
# Returns [{'box': LIST_OF_COORDINATES, 'score': PROBABILITY, 'label': LABEL}, ...]
print(l)
print(type(l))
print(l[0]['score'])
print(l[0]['box'][0],",",l[0]['box'][1])
point=l[0]['box'][0],l[0]['box'][1]
pyautogui.moveTo(point)
pyautogui.leftClick()
#pyautogui.hotkey('alt', 'f4')