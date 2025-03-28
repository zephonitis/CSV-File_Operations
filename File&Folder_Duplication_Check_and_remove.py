import pandas as pd
import os
from tkinter import Tk, filedialog

def remove_duplicates_across_files(reference_file, folder):
    # Load the reference file and extract emails (standardize to lower-case & trimmed)
    ref_df = pd.read_csv(reference_file)
    ref_emails = set(ref_df['email'].astype(str).str.lower().str.strip())
    
    encountered_emails = set()  # To track emails seen across folder files

    # Get a sorted list of all CSV files in the folder
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.csv')]
    files.sort()  # Sorting to establish a consistent order

    for file in files:
        print(f"\nProcessing file: {file}")
        df = pd.read_csv(file)

        # Check if 'email' column exists in the current file
        if 'email' not in df.columns:
            print(f"Skipping {file}: 'email' column not found.")
            continue

        # Standardize the email field (lowercase and strip whitespace)
        df['email'] = df['email'].astype(str).str.lower().str.strip()
        
        # Capture duplicates within the file (internal duplicates based on email)
        internal_duplicates = df[df.duplicated(subset=['email'], keep='first')]
        if not internal_duplicates.empty:
            print("Internal duplicate records (within same file) to be removed:")
            print(internal_duplicates)
        
        # Remove internal duplicates (keeping first occurrence)
        df = df.drop_duplicates(subset=['email'])
        
        # Capture duplicates with the reference file
        mask_ref = df['email'].isin(ref_emails)
        ref_duplicates = df[mask_ref]
        if not ref_duplicates.empty:
            print("Records found in reference file (to be removed):")
            print(ref_duplicates)
        # Remove rows that are duplicates with the reference file
        df = df[~mask_ref]
        
        # Capture duplicates with previously processed files
        mask_encountered = df['email'].isin(encountered_emails)
        cross_duplicates = df[mask_encountered]
        if not cross_duplicates.empty:
            print("Records duplicated across folder files (to be removed):")
            print(cross_duplicates)
        # Remove rows that are duplicates across previously processed files
        df = df[~mask_encountered]
        
        # Update encountered_emails with emails from the current file
        encountered_emails.update(df['email'].tolist())
        
        # Overwrite the current file with the cleaned data
        df.to_csv(file, index=False)
        print(f"Updated file saved: {file}")

if __name__ == "__main__":
    Tk().withdraw()  # Hide the Tkinter root window

    # Prompt user to select the reference file (this file remains unchanged)
    reference_file = filedialog.askopenfilename(title="Select Reference CSV File (Do not modify)")
    
    # Prompt user to select the folder containing CSV files to process
    folder = filedialog.askdirectory(title="Select Folder with CSV Files to Process")
    
    if reference_file and folder:
        remove_duplicates_across_files(reference_file, folder)
    else:
        print("Reference file or folder not selected.")

