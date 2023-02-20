# Main.py
import os
import re
import time
import winsound
from datetime import datetime

# File Path and Listener Name.
directory_path = "C:\\Users\\mrwil\\OneDrive\\Documents\\EVE\\logs\\Gamelogs"  # replace with your directory path
listener_name = "WildGear"

# Get a list of all the files in the directory
all_files = os.listdir(directory_path)

# Filter the list to include only files that contain the listener name in their header
listener_files = (file for file in all_files if os.path.isfile(os.path.join(directory_path, file))
                  and re.search(f"Listener:\\s*{listener_name}", open(os.path.join(directory_path, file)).read()))
listener_files = list(listener_files)

# Sort the list of listener files by their session start time (in descending order)
listener_files.sort(key=lambda file: datetime.strptime(
    re.search(r"Session Started: (.+)", open(os.path.join(directory_path, file)).read()).group(1), "%Y.%m.%d %H:%M:%S"),
                    reverse=True)

# Define the keys and messages to search for
# Define key_messages dictionary
key_messages = {
     "set1": (["Centus Beast Lord", "Centus Mutant Lord", "Centus Plague Lord", "Centus Savage Lord"], "BattleShip Wave"),
     "set2": (["True Centatis Behemoth", "True Centatis Daemon", "True Centatis Devil", "True Centatis Phantasm", "True Centatis Specter", "True Centatis Wraith"], "Faction Spawn")
}
# Define session_started_regex
session_started_regex = re.compile(r"Session Started: (.+)")

# Define a variable to store the last time the sound effect was played
last_sound_played_time = time.time()

# Define the path to the sound effect
sound_effect_path = "path/to/sound/effect.wav"

# Start an infinite loop to continuously run the search until a stop command is issued
while True:
    # Get the latest listener file, if any
    latest_listener_file = listener_files[0] if listener_files else None

    # Define the file path and check if the file exists
    if latest_listener_file:
        file_path = os.path.join(directory_path, latest_listener_file)
        if os.path.exists(file_path):
            # Get the current size of the file
            file_size = os.path.getsize(file_path)

            # Define the line number to start reading from
            start_line_number = 0

            # Start an infinite loop to keep searching until the user types "stop"
            while True:
                # Get the current size of the file
                current_file_size = os.path.getsize(file_path)

                # If the file size has decreased, reset the line number to 0
                if current_file_size < file_size:
                    start_line_number = 0
                    file_size = current_file_size

                # Read the lines starting from the start_line_number
                with open(file_path, "r") as file:
                    file.seek(start_line_number)
                    for line in file:
                        for keys, message in key_messages.values():
                            if any(key in line for key in keys):
                                print(f"{message} ({', '.join(keys)})")
                                # Check if 65 seconds have passed since the last sound was played
                                if time.time() - last_sound_played_time >= 80:
                                    # Play the sound effect
                                    winsound.PlaySound(sound_effect_path, winsound.SND_FILENAME)

                                    # Update the last sound played time
                                    last_sound_played_time = time.time()

                    start_line_number = file.tell()

                time.sleep(1)  # pause for 1 second
        else:
            # If the file does not exist, remove it from the list of
            if not listener_files:
                # Display a message and wait for a minute before checking for new files
                print("No listener file found. Checking again in 1 minute.")
                time.sleep(60)
            else:
                latest_listener_file = listener_files[0]
                file_path = os.path.join(directory_path, latest_listener_file)
                if not os.path.exists(file_path):
                    raise Exception("File does not exist!")
                file_size = os.path.getsize(file_path)
                start_line_number = 0
                while True:
                    current_file_size = os.path.getsize(file_path)
                    if current_file_size < file_size:
                        start_line_number = 0
                        file_size = current_file_size
                    with open(file_path, "r") as file:
                        file.seek(start_line_number)
                        for line in file:
                            for key_set, (keys, message) in key_messages.items():
                                if any(key in line for key in keys):
                                    print(f"{message} ({', '.join(keys)})")
                                    if time.time() - last_sound_played_time >= 80:
                                        winsound.PlaySound("path/to/sound/effect.wav", winsound.SND_FILENAME)
                                        last_sound_played_time = time.time()
                        start_line_number = file.tell()
                    time.sleep(5)
