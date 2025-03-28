import os
import pandas as pd
from tkinter import Tk, filedialog

def normalize(col):
    """Normalize a column name by converting it to lowercase and replacing spaces with underscores."""
    return col.lower().replace(" ", "_")

def process_files(template_file, data_folder):
    # Read the template file to get desired columns
    try:
        template_df = pd.read_csv(template_file, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(f"Error reading template file: {e}")
        return

    # Normalize template columns and create mapping:
    # key: normalized column name, value: original template column name.
    template_columns = list(template_df.columns)
    normalized_template_mapping = {normalize(col): col for col in template_columns}
    print("Template columns:", template_columns)
    
    # Use the directory of the template file as the output folder
    output_folder = os.path.dirname(template_file)
    
    # Get all CSV files from the data folder
    data_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.lower().endswith('.csv')]
    
    for data_file in data_files:
        print(f"\nProcessing data file: {data_file}")
        try:
            # Read data file, skipping bad lines if any
            data_df = pd.read_csv(data_file, on_bad_lines='skip', engine='python')
        except Exception as e:
            print(f"Error reading {data_file}: {e}")
            continue

        # Build a renaming dictionary by normalizing each column in the data file 
        # and comparing with the template mapping. 
        rename_dict = {}
        for col in data_df.columns:
            norm_col = normalize(col.strip())
            if norm_col in normalized_template_mapping:
                rename_dict[col] = normalized_template_mapping[norm_col]
            # Special case: if normalized column equals 'work_email', map it to 'email'
            elif norm_col == "work_email" and "email" in normalized_template_mapping.values():
                rename_dict[col] = "email"
                
        # Rename the data file columns accordingly
        data_df = data_df.rename(columns=rename_dict)
        
        # Determine common columns between the template and the current data file
        common_columns = [col for col in template_columns if col in data_df.columns]
        if not common_columns:
            print(f"No matching columns found in {data_file}. Skipping this file.")
            continue
        
        # Reindex the DataFrame to follow the template's column order.
        # Missing columns (if any) will be added as NaN.
        formatted_df = data_df.reindex(columns=template_columns)
        
        # Remove duplicate rows (based on all columns)
        before_count = len(formatted_df)
        formatted_df = formatted_df.drop_duplicates()
        after_count = len(formatted_df)
        duplicates_removed = before_count - after_count
        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate row(s) from {data_file}.")
        
        # Create output file name (in the template folder)
        base_name = os.path.basename(data_file)
        output_file = os.path.join(output_folder, f"formatted_{base_name}")
        
        try:
            formatted_df.to_csv(output_file, index=False)
            print(f"Formatted file saved as: {output_file}")
        except Exception as e:
            print(f"Error saving file {output_file}: {e}")

if __name__ == "__main__":
    Tk().withdraw()  # Hide the Tkinter window

    # Prompt for the template CSV file (should contain only column names)
    template_file = filedialog.askopenfilename(title="Select Template CSV File (with only column names)")
    
    # Prompt for the folder containing data CSV files (which may have varying schema)
    data_folder = filedialog.askdirectory(title="Select Folder with Data CSV Files")
    
    if template_file and data_folder:
        process_files(template_file, data_folder)
    else:
        print("Template file or data folder not selected.")


