import PySimpleGUI as sg
from nudenet import NudeClassifier
import os.path

def Validpath(filepath):
    if os.path.isfile(filepath):
        return True
    sg.popup_error("Filepath Missing or Incorrect")
    return False

def tostr(per):
    per = str(per)
    per = per+"%"
    return per

def main():
    sg.theme('Reds')
    layout = [
        [sg.Text("Choose a file: "), sg.Input(key="File"), sg.FileBrowse(file_types=(("JPG Images","*.jpg"),))],
        [sg.Button('Submit')]
    ]
    
    # Building Window
    window = sg.Window('My File Browser', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            # Close the window if the close button is clicked
            break
        
        if event == 'Submit':
            classifier = NudeClassifier()
            image_path=values["File"]
            if Validpath(image_path):
                a = classifier.classify(image_path)
                unsafe_per=round(100*a[image_path]['unsafe'],2)
                safe_per=round(100*a[image_path]['safe'],2)
                
                print("Unsafe",unsafe_per,"%")
                print("Safe",safe_per,"%")
                
                if safe_per >70 :
                    safe_per=tostr(safe_per)
                    sg.popup_auto_close("Safe",safe_per)
                else:
                    unsafe_per=tostr(unsafe_per)
                    sg.popup_auto_close("Unsafe",unsafe_per)
    window.close()

main()