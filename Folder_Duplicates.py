import os
import pandas as pd
from tkinter import filedialog, Tk

def remove_duplicates_by_email(folder_path):
    # Get all CSV file paths
    csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.csv')]
    file_paths = [os.path.join(folder_path, f) for f in csv_files]

    dataframes = []
    file_info = []

    print("Reading CSV files...")
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig', engine='python', on_bad_lines='skip')
            
            if 'email' not in df.columns:
                print(f"Skipping {file_path} (no 'email' column found).")
                continue

            dataframes.append(df)
            file_info.append((file_path, df.shape[0]))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    if not dataframes:
        print("No valid CSV files with an 'email' column found.")
        return

    # Combine all rows and drop duplicates based on 'email'
    combined_df = pd.concat(dataframes, ignore_index=True)
    print(f"Total rows before removing email duplicates: {len(combined_df)}")

    combined_df = combined_df.drop_duplicates(subset='email', keep='first')
    print(f"Total rows after removing email duplicates: {len(combined_df)}")

    # Reassign unique rows back to files
    current_index = 0
    for file_path, original_len in file_info:
        df_slice = combined_df.iloc[current_index : current_index + original_len]
        current_index += len(df_slice)

        try:
            df_slice.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"Updated: {file_path} ({len(df_slice)} rows)")
        except Exception as e:
            print(f"Error saving {file_path}: {e}")

if __name__ == "__main__":
    Tk().withdraw()
    folder = filedialog.askdirectory(title="Select Folder Containing CSV Files")
    if folder:
        remove_duplicates_by_email(folder)
    else:
        print("No folder selected.")
