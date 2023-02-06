import os
from tkinter import filedialog
import tkinter as tk


class DirectoryReader:
    def __init__(self):
        self.directory = tk.StringVar()

    def select_directory(self):
        dire = filedialog.askdirectory()
        self.directory.set(dire)

    def get_all_files_directories(self):
        if os.path.isdir(self.directory.get()) and (len(os.listdir(self.directory.get())) != 0):
            all_directories = []
            for file in os.listdir(self.directory.get()):
                all_directories.append(os.path.join(self.directory.get(), file))
            return all_directories
        else:
            return None

    def get_accounts_file_directories(self, names: list) -> dict:
        all_files = self.get_all_files_directories()
        accounts_files = {}
        if all_files is not None:
            for name in names:
                for file in all_files:
                    with open(file, 'r') as f:
                        if f.readline(2).strip().__contains__("Listener:" + name.strip()):
                            accounts_files[name] = file
        return accounts_files
