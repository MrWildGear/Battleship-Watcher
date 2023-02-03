#
#  Version 0.1
#
#   Centus Beast Lord,Centus Mutant Lord,Centus Savage Lord,True Sansha
# 
import winsound
import tkinter as tk
import os
import time
from tkinter import filedialog

class LogFileNotFoundError(Exception):
    pass

class KeywordTracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Battleship Watcher")
        self.geometry("400x200")
        self.resizable(True, True)
        self.folder_location = tk.StringVar()
        self.folder_location.set("")
        self.keywords = tk.StringVar()
        self.keywords.set("Centus Beast Lord,Centus Mutant Lord,Centus Savage Lord,True Sansha")
        self.count = tk.IntVar()
        self.count.set(0)

        self.folder_location_label = tk.Label(self, text="Folder Location")
        self.folder_location_label.pack()

        self.folder_location_entry = tk.Entry(self, textvariable=self.folder_location)
        self.folder_location_entry.pack()
    
        self.browse_button = tk.Button(self, text="Browse", command=self.select_folder)
        self.browse_button.pack()

        self.keywords_label = tk.Label(self, text="Keywords (comma-separated)")
        self.keywords_label.pack()

        self.keywords_entry = tk.Entry(self, textvariable=self.keywords)
        self.keywords_entry.pack()

        self.count_label = tk.Label(self, textvariable=self.count)
        self.count_label.pack()

        self.start_button = tk.Button(self, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack()

    def select_folder(self):
        folder_location = filedialog.askdirectory()
        self.folder_location.set(folder_location)

    def start_monitoring(self):
        while True:
            folder_location = self.folder_location.get()
            keywords_to_watch = self.keywords.get().split(',')


            dir_list = [f for f in os.listdir(folder_location)]
            # , key=os.path.getctime
            latest_file = max(dir_list)

            filename = os.path.join(folder_location, latest_file)

            lines = self.read_log_file(filename)

            monitored_Data = self.extract_keywords(lines)
            self.trigger_audio_cue(monitored_Data, keywords_to_watch)
            time.sleep(20000)
            continue

    def extract_keywords(self, lines):
        clean_lines = []
        for line in lines:
            if line.__contains__("combat"):
                clean_lines.append((line.split("-"))[0])
        # {word for line in lines for word in line.strip().split(',')}
        return clean_lines

    def read_log_file(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise LogFileNotFoundError("File not found")
        return lines

    def trigger_audio_cue(self, monitored_Data, keywords_to_watch):
        for keyword in keywords_to_watch:
            for entry in monitored_Data:
                if entry.__contains__(keyword):
                    winsound.PlaySound("sound.wav", winsound.SND_FILENAME)
                    print("it did iiiiiiiiiiiit")
                    return True
        return False

app = KeywordTracker()
app.mainloop()



#   Centus Beast Lord,Centus Mutant Lord,Centus Savage Lord,True Sansha
