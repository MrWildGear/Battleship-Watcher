import threading

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
        self.folder_location = tk.StringVar()
        self.folder_location.set("C:/Users/abdal/Documents/EVE/logs/Gamelogs")

        self.keywords = tk.StringVar()
        self.keywords.set(
            "Corpus Patriarch,Corpus Pope,Centus Beast Lord,Centus Mutant Lord,Centus Savage Lord,True Sansha")

        self.count = tk.IntVar()
        self.count.set(0)

        self.monitoring = threading.Event()
        self.thread = threading.Thread()

        """
        setting all Window Widgets and settings
        """
        self.title("Battleship Watcher")
        self.geometry("400x250")
        self.resizable(True, False)

        self.folder_location_label = tk.Label(self, text="Folder Location")
        self.folder_location_label.pack()

        self.folder_location_entry = tk.Entry(self, textvariable=self.folder_location)
        self.folder_location_entry.pack()

        self.browse_button = tk.Button(self,
                                       text="Browse",
                                       command=lambda: {
                                           self.folder_location.set(filedialog.askdirectory())
                                       })
        self.browse_button.pack()

        self.keywords_label = tk.Label(self, text="Keywords (comma-separated)")
        self.keywords_label.pack()

        self.keywords_entry = tk.Entry(self, textvariable=self.keywords)
        self.keywords_entry.pack()

        self.count_label = tk.Label(self, textvariable=self.count)
        self.count_label.pack()

        self.start_button = tk.Button(self, text="Start Monitoring", command=self.make_thread_and_start_monitoring)
        self.start_button.pack()

        self.folder_location_label = tk.Label(self, text="Monitor Every")
        self.folder_location_label.pack()

        self.number = tk.Spinbox(self, from_=1, to=500, width=5)
        self.number.pack()

        self.start_button = tk.Button(self, text="Stop Monitoring", command=self.stop_monitoring)
        self.start_button.pack()

    """
    delete the old thread if there was. 
    reinitialize the self.thread variable with a new thread
    starts the new thread
    """

    def make_thread_and_start_monitoring(self):
        del self.thread
        self.thread = threading.Thread(target=self.start_monitoring)
        self.monitoring.clear()
        self.thread.start()

    """
    on a period of a number of seconds equal to self.number value call self.trigger_audio_cue 
    with the most recent appropriate arguments
    """
    def start_monitoring(self):
        while not self.monitoring.is_set():
            folder_location = self.folder_location.get()
            all_files = os.listdir(folder_location)
            latest_file = max(all_files)
            filename = os.path.join(folder_location, latest_file)
            lines = self.read_log_file(filename)

            self.trigger_audio_cue(
                self.extract_keywords(lines),
                self.keywords.get().split(','))
            print(0)
            self.monitoring.wait(int(self.number.get()))
            continue
        else:
            return

    """
    stop the periodic scanning loop to return out of the thread
    and then clean it up
    """
    def stop_monitoring(self):
        if not self.monitoring.is_set() and self.thread.is_alive():
            self.monitoring.set()
            self.thread.join()
            print(1)

    """
    cleans the parameter lines with the character '_' and returns a clean list
    """
    def extract_keywords(self, lines):
        clean_lines = []
        for line in lines:
            if line.__contains__("combat"):
                clean_lines.append((line.split("-"))[0])
        # {word for line in lines for word in line.strip().split(',')}
        return clean_lines

    """
    opens the file of the directory 'filename' and returns all the lines in a list
    """
    def read_log_file(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise LogFileNotFoundError("File not found")
        return lines

    """
    searches for matching words in the monitored_Data using the keywords_to_watch list and triggers a sound on success
    """
    def trigger_audio_cue(self, monitored_Data, keywords_to_watch):
        for keyword in keywords_to_watch:
            for entry in monitored_Data:
                if entry.__contains__(keyword):
                    winsound.PlaySound("sound.wav", winsound.SND_FILENAME)
                    return True
        return False

    """
    overriding the close function and stopping monitoring before the app ends
    """
    def destroy(self):
        super().destroy()
        self.stop_monitoring()


if __name__ == '__main__':
    app = KeywordTracker()
    app.mainloop()

#   Centus Beast Lord,Centus Mutant Lord,Centus Savage Lord,True Sansha
