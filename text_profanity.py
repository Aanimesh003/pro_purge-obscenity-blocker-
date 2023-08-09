from PIL import Image
from pytesseract import pytesseract
import tkinter as tk
from tkinter import messagebox
from better_profanity import profanity
import time

# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
image_path = r"pic.png"

# Opening the image & storing it in an image object



def save_text_to_file():
    file1 = open(r"text.txt", "w")
    file1.write(text[:-1])
    file1.close()


def show_warning():
    messagebox.showwarning("Warning", "Obscene text detected!")
    
def checking_profanity():
    dirty_text = 'text.txt'

    if profanity.contains_profanity(dirty_text):
        print("Showing Warning!")
        show_warning()


while True:
    time.sleep(1)
    img = Image.open(image_path)
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(img)
    save_text_to_file()
    dirty_text = 'text.txt'
    profanity.contains_profanity(dirty_text)
    