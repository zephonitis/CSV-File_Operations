import pandas as pd
from tkinter import Tk, filedialog

def normalize_column_names(columns):
    column_mapping = {col: col.lower().replace(" ", "_") for col in columns}
    
    # Ensure 'work_email' is mapped to 'email'
    column_mapping = {key: "email" if value == "work_email" else value for key, value in column_mapping.items()}
    
    # Ensure 'company_name' is mapped to 'company'
    column_mapping = {key: "company" if value == "company_name" else value for key, value in column_mapping.items()}

    return column_mapping

def merge_csv_files(file1, file2, output_file):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Normalize column names for df2
    df2.rename(columns=normalize_column_names(df2.columns), inplace=True)

    # Ensure df2 has only the columns present in df1
    df2 = df2[df1.columns.intersection(df2.columns)]

    # Merge data and remove duplicates
    merged_df = pd.concat([df1, df2], ignore_index=True)
    merged_df.drop_duplicates(inplace=True)

    # Save the merged file
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved as: {output_file}")

if __name__ == "__main__":
    Tk().withdraw()  # Hide the root window
    file1 = filedialog.askopenfilename(title="Select File 1 (Primary CSV)")
    file2 = filedialog.askopenfilename(title="Select File 2 (Secondary CSV)")
    output_file = filedialog.asksaveasfilename(title="Save Merged File As", defaultextension=".csv")

    if file1 and file2 and output_file:
        merge_csv_files(file1, file2, output_file)
    else:
        print("File selection was canceled.")
