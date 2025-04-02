import os
import pandas as pd
from tkinter import Tk, filedialog

def merge_csv_files(folder_path, output_file):
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.csv')]
    
    if not all_files:
        print("No CSV files found in the folder.")
        return
    
    merged_df = pd.DataFrame()
    
    for idx, file in enumerate(all_files):
        try:
            df = pd.read_csv(file)
            
            # If it's the first file, keep the header
            if idx == 0:
                merged_df = df
            else:
                merged_df = pd.concat([merged_df, df], ignore_index=True)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
    
    # Remove duplicate rows
    before_count = len(merged_df)
    merged_df.drop_duplicates(inplace=True)
    after_count = len(merged_df)
    duplicates_removed = before_count - after_count
    
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate row(s).")
    
    # Save the merged file without extra headers
    try:
        merged_df.to_csv(os.path.join(folder_path, output_file), index=False)
        print(f"Merged file saved as: {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    Tk().withdraw()  # Hide the Tkinter window
    folder_selected = filedialog.askdirectory(title="Select Folder with CSV Files")
    
    if folder_selected:
        output_filename = "merged_output.csv"
        merge_csv_files(folder_selected, output_filename)
    else:
        print("No folder selected.")
