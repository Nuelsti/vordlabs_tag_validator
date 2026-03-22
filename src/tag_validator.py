from pathlib import Path
import pandas as pd
import sys
import os
import re

# Debug: show which Python and current working directory (helps VS Code F6 issues)
print("sys.executable:", sys.executable)
print("cwd:", os.getcwd())

# load the tag data (path resolved relative to this script file)
script_dir = Path(__file__).resolve().parent
file_path = script_dir.parent / "data" / "Valve_list.xlsx"
df = pd.read_excel(file_path)

#clean the tag data

df['VALVE TAG'] = df['VALVE TAG'].astype(str).str.strip()

#Detect duplicates in the 'VALVE TAG' column

duplicate_counts = df['VALVE TAG'].value_counts()
duplicates = duplicate_counts[duplicate_counts > 1]

# Format validation
pattern = r'^[A-Z]{2,3}-\d{3}$'

invalid_format = []

# Validate tags: skip missing values and coerce to string before matching
for tag in df['VALVE TAG']:
    if pd.isna(tag):
        continue
    t = str(tag).strip()
    if not re.match(pattern, t):
        invalid_format.append(t)


# OUTPUT
print("=== TAGs VALIDATOR REPORT === \n")

# DUPLICATES
print("Duplicate VALVE TAGs:")
if not duplicates.empty:
    for tag, count in duplicates.items():
        print(f"VALVE TAG '{tag}': {count} occurrences")
else:    print("No duplicate VALVE TAGs found.")

print("\nInvalid Format VALVE TAGs:")
if invalid_format:
    for tag in invalid_format:
        print(f"VALVE TAG '{tag}' does not match the required format.")
else:    print("All VALVE TAGs match the required format.")


# save the duplicates to a new Excel file (path resolved relative to this script)
output_dir = script_dir.parent / "output"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "invalid_format_report.xlsx"
duplicates.to_excel(output_path, index=True)
pd.DataFrame(invalid_format, columns=['Invalid VALVE TAGs']).to_excel(output_path, index=False, startrow=len(duplicates) + 2)
# Append invalid format tags below duplicates
print(f"\nInvalid Format VALVE TAGs have been saved to '{output_path}'")