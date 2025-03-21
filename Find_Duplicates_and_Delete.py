import pandas as pd
from tkinter import Tk, filedialog

def remove_duplicates(file1, file2, output_file):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Find common columns between both files
    common_columns = df1.columns.intersection(df2.columns)
    
    # Keep only the common columns in both dataframes
    df1 = df1[common_columns]
    df2 = df2[common_columns]
    
    # Find duplicate rows in df2 that match rows in df1
    duplicates = df2[df2.apply(tuple, axis=1).isin(df1.apply(tuple, axis=1))]
    
    if duplicates.empty:
        print("No duplicate rows found in the second file.")
    else:
        print("Duplicate rows found and will be removed.")
        df2 = df2[~df2.apply(tuple, axis=1).isin(df1.apply(tuple, axis=1))]
        df2.to_csv(output_file, index=False)
        print(f"Updated file saved as: {output_file}")

if __name__ == "__main__":
    Tk().withdraw()  # Hide the root window
    file1 = filedialog.askopenfilename(title="Select File 1 (Reference CSV)")
    file2 = filedialog.askopenfilename(title="Select File 2 (Target CSV)")
    output_file = filedialog.asksaveasfilename(title="Save Cleaned File As", defaultextension=".csv")
    
    if file1 and file2 and output_file:
        remove_duplicates(file1, file2, output_file)
    else:
        print("File selection was canceled.")
