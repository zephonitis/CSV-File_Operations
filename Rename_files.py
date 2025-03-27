import os
from tkinter import Tk, filedialog

def rename_files_in_directory(directory):
    files = sorted(os.listdir(directory))  # Get and sort files in the directory
    
    count = 1
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):  # Ensure it's a file, not a folder
            extension = os.path.splitext(file)[1]  # Get file extension
            new_name = os.path.join(directory, f"{count}{extension}")
            os.rename(file_path, new_name)
            count += 1
    
    print(f"Renamed {count - 1} files successfully!")

if __name__ == "__main__":
    Tk().withdraw()  # Hide the Tkinter GUI window
    folder_selected = filedialog.askdirectory(title="Select Folder to Rename Files")
    
    if folder_selected:
        rename_files_in_directory(folder_selected)
    else:
        print("No folder selected. Exiting.")
