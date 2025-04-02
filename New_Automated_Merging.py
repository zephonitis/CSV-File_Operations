import os
import pandas as pd
import csv
from tkinter import Tk, filedialog

def normalize(col):
    """Normalize a column name by converting it to lowercase and replacing spaces with underscores."""
    return col.lower().replace(" ", "_")

def detect_delimiter(file_path):
    """Detect delimiter using csv.Sniffer."""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        sample = f.read(1024)
        sniffer = csv.Sniffer()
        return sniffer.sniff(sample).delimiter

def process_files(template_file, data_folder):
    # Read the template file to get desired columns
    try:
        template_df = pd.read_csv(template_file, encoding='utf-8-sig', on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading template file: {e}")
        return

    # Normalize template columns and create mapping
    template_columns = list(template_df.columns)
    normalized_template_mapping = {normalize(col): col for col in template_columns}
    print("Template columns:", template_columns)
    
    output_folder = os.path.dirname(template_file)
    data_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.lower().endswith('.csv')]
    
    for data_file in data_files:
        print(f"\nProcessing data file: {data_file}")
        try:
            delimiter = detect_delimiter(data_file)
            data_df = pd.read_csv(
                data_file,
                encoding='utf-8-sig',
                delimiter=delimiter,
                quotechar='"',
                on_bad_lines='skip',
                dtype=str  # Read all as string to avoid unwanted parsing issues
            )
        except Exception as e:
            print(f"Error reading {data_file}: {e}")
            continue

        # Build a renaming dictionary
        rename_dict = {}
        for col in data_df.columns:
            norm_col = normalize(col.strip())
            if norm_col in normalized_template_mapping:
                rename_dict[col] = normalized_template_mapping[norm_col]
            elif norm_col == "work_email" and "email" in normalized_template_mapping.values():
                rename_dict[col] = "email"
        
        data_df = data_df.rename(columns=rename_dict)
        
        # Determine common columns
        common_columns = [col for col in template_columns if col in data_df.columns]
        if not common_columns:
            print(f"No matching columns found in {data_file}. Skipping this file.")
            continue
        
        formatted_df = data_df[common_columns]
        
        # Remove duplicate rows
        before_count = len(formatted_df)
        formatted_df = formatted_df.drop_duplicates()
        after_count = len(formatted_df)
        duplicates_removed = before_count - after_count
        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate row(s) from {data_file}.")
        
        output_file = os.path.join(output_folder, f"formatted_{os.path.basename(data_file)}")
        
        try:
            formatted_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"Formatted file saved as: {output_file}")
        except Exception as e:
            print(f"Error saving file {output_file}: {e}")

if __name__ == "__main__":
    Tk().withdraw()
    template_file = filedialog.askopenfilename(title="Select Template CSV File (with only column names)")
    data_folder = filedialog.askdirectory(title="Select Folder with Data CSV Files")
    
    if template_file and data_folder:
        process_files(template_file, data_folder)
    else:
        print("Template file or data folder not selected.")
