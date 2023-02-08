from Main_App.DataSource.directory_reader import DirectoryReader
from Main_App.Utils.data_processing import read_file


class FileReader:
    def __init__(self, directory_reader: DirectoryReader):
        self.directory_reader = directory_reader
        self.character_names = []

    def read_last_file(self) -> list or Exception:
        all_files_directories = self.directory_reader.get_all_files_directories()
        if all_files_directories is not None:
            filename = max(self.directory_reader.get_all_files_directories())
            return read_file(filename)
        else:
            return None

    def read_character_file(self):
        pass
