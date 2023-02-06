import threading

import winsound
import tkinter as tk
import os
from tkinter import filedialog

from Main_App.DataSource.directory_reader import DirectoryReader
from Main_App.DataSource.file_reader import FileReader
from Main_App.Utils.data_processing import filter_lines_by, read_file
from Main_App.Utils.data_searchers import count_for_list_items_in_list


class KeywordTracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # self.folder_location = tk.StringVar()
        # self.folder_location.set("")

        self.keywords = tk.StringVar()
        self.keywords.set(
            "Corpus Patriarch,Corpus Pope,Centus Beast Lord,Centus Mutant Lord,Centus Savage Lord,True Sansha")

        self.count = tk.IntVar()
        self.count.set(0)

        self.monitoring = threading.Event()
        self.thread = threading.Thread()

        self.repo = FileReader(DirectoryReader())

        """
        setting all Window Widgets and settings
        """
        self.title("Battleship Watcher")
        self.geometry("400x250")
        self.resizable(True, False)

        self.folder_location_label = tk.Label(self, text="Folder Location")
        self.folder_location_label.pack()

        self.folder_location_entry = tk.Entry(self, textvariable=self.repo.directory_reader.directory)
        self.folder_location_entry.pack()

        self.browse_button = tk.Button(self,
                                       text="Browse",
                                       command=self.repo.directory_reader.select_directory)
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

    def make_thread_and_start_monitoring(self):
        """
        delete the old thread if there was.
        reinitialize the thread variable with a new thread
        starts the new thread
        """
        self.thread = threading.Thread(target=self.start_monitoring)
        self.monitoring.clear()
        self.thread.start()

    def start_monitoring(self):
        """
        on a period of a number of seconds equal to number value call self.trigger_audio_cue
        with the most recent appropriate arguments
        """
        while not self.monitoring.is_set():
            lines = self.repo.read_last_file()
            if lines is not None:
                self.count.set(
                    count_for_list_items_in_list(filter_lines_by(lines, "combat"), self.keywords.get().split(','))
                )
                if self.count.get() > 0:
                    winsound.PlaySound("sound.wav", winsound.SND_FILENAME)

                self.monitoring.wait(int(self.number.get()))
                continue
            else:
                return Exception("can't get lines")
        else:
            return

    def stop_monitoring(self):
        """
        stop the periodic scanning loop to return out of the thread
        and then clean it up
        """
        if not self.monitoring.is_set() and self.thread.is_alive():
            self.monitoring.set()
            self.thread.join()
            del self.thread

    def destroy(self):
        """
        overriding the close function and stopping monitoring before the app ends
        """
        super().destroy()
        self.stop_monitoring()


if __name__ == '__main__':
    app = KeywordTracker()
    app.mainloop()

#   Centus Beast Lord,Centus Mutant Lord,Centus Savage Lord,True Sansha
