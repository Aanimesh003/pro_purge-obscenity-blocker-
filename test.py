import detector
import pyautogui
nd = detector

while True:
    screen=pyautogui.screenshot("screen.png")
    detct=nd.detect("screen.png")