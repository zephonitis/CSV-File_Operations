# Merge CSV Tool

This Python script merges two CSV files while:
- Ensuring no duplicate records in the final file.
- Retaining only the columns from File 1.
- Mapping column names from File 2 to match File 1 (e.g., converting "Work email" to "email").
- Handling uppercase and spaces in column names.

## How to Use
1. Run `python merge_csv.py` in VS Code.
2. Select the CSV files when prompted.
3. The merged file is saved as per your selection.

## Requirements
- Python 3.x
- Pandas (`pip install pandas`)

## License
MIT License
