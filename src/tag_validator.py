from pathlib import Path
import pandas as pd
import sys
import os

# Debug: show which Python and current working directory (helps VS Code F6 issues)
print("sys.executable:", sys.executable)
print("cwd:", os.getcwd())

# load the tag data (path resolved relative to this script file)
script_dir = Path(__file__).resolve().parent
file_path = script_dir.parent / "data" / "Valve_list.xlsx"
df = pd.read_excel(file_path)
# print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns from {file_path}")


#clean the tag data
# df['Valve Tag'] = df['VAL Tag'].astype(str).str.strip()
# print(df['VALVE TAG'])
df['VALVE TAG'] = df['VALVE TAG'].astype(str).str.strip()

#Detect duplicates in the 'VALVE TAG' column
# duplicates = df[df.duplicated(subset=['VALVE TAG'], keep=False)]
# if not duplicates.empty:
#     print("Duplicate VALVE TAGs found:")
#     print(duplicates[['VALVE TAG']])
# else:    print("No duplicate VALVE TAGs found.")
duplicate_counts = df['VALVE TAG'].value_counts()
duplicates = duplicate_counts[duplicate_counts > 1]

print("=== Duplicate VALVE TAGs Report === \n")
for tag, count in duplicates.items():
    print(f"VALVE TAG '{tag}': {count} occurrences")

# save the duplicates to a new Excel file (path resolved relative to this script)
output_dir = script_dir.parent / "output"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "duplicate_valve_tag.xlsx"
duplicates.to_excel(output_path, index=True)
print(f"\nDuplicate VALVE TAGs have been saved to '{output_path}'")