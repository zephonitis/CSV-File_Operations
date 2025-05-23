import os
import pandas as pd
from tkinter import Tk, filedialog

def normalize(col):
    return col.lower().replace(" ", "_")

def process_files(template_file, data_folder):
    try:
        template_df = pd.read_csv(template_file, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(f"Error reading template file: {e}")
        return

    template_columns = list(template_df.columns)
    normalized_template_mapping = {normalize(col): col for col in template_columns}
    print("Template columns:", template_columns)
    
    output_folder = os.path.dirname(template_file)
    data_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.lower().endswith('.csv')]
    
    combined_df = pd.DataFrame()

    for data_file in data_files:
        print(f"\nProcessing data file: {data_file}")
        try:
            df = pd.read_csv(data_file, on_bad_lines='skip', engine='python', encoding='utf-8-sig', quoting=1)
        except Exception as e:
            print(f"Error reading {data_file}: {e}")
            continue

        rename_dict = {}
        for col in df.columns:
            norm_col = normalize(col.strip())
            if norm_col in normalized_template_mapping:
                rename_dict[col] = normalized_template_mapping[norm_col]
            elif norm_col == "work_email" and "email" in normalized_template_mapping.values():
                rename_dict[col] = "email"
            elif norm_col == "company_name" and "company" in normalized_template_mapping.values():
                rename_dict[col] = "company"

        df = df.rename(columns=rename_dict)

        # Align columns to template and drop duplicates
        formatted_df = df.reindex(columns=template_columns)
        formatted_df = formatted_df.drop_duplicates()

        # Filter rows with valid email
        formatted_df = formatted_df[formatted_df['email'].notnull() & (formatted_df['email'].str.strip() != '')]

        combined_df = pd.concat([combined_df, formatted_df], ignore_index=True)

    # Final clean-up
    combined_df = combined_df.drop_duplicates()

    # Chunk size
    chunk_size = 172
    total_rows = len(combined_df)
    num_files = (total_rows + chunk_size - 1) // chunk_size

    print(f"\nTotal valid contacts: {total_rows}")
    print(f"Generating {num_files} output file(s) with up to {chunk_size} contacts each...")

    for i in range(num_files):
        chunk = combined_df.iloc[i * chunk_size : (i + 1) * chunk_size]
        output_file = os.path.join(output_folder, f"formatted_contacts_part_{i+1}.csv")
        try:
            chunk.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"Saved: {output_file}")
        except Exception as e:
            print(f"Error saving {output_file}: {e}")

if __name__ == "__main__":
    Tk().withdraw()

    template_file = filedialog.askopenfilename(title="Select Template CSV File (with only column names)")
    data_folder = filedialog.askdirectory(title="Select Folder with Data CSV Files")
    
    if template_file and data_folder:
        process_files(template_file, data_folder)
    else:
        print("Template file or data folder not selected.")
