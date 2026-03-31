from pathlib import Path
import pandas as pd
import sys
import os
import re
# wrapping the main code in a function to avoid issues with VS Code F6 execution
def run_validator(file_path, output_path):
    # Debug: show which Python and current working directory (helps VS Code F6 issues)
    # print("sys.executable:", sys.executable)
    # print("cwd:", os.getcwd())

    # load the tag data (path resolved relative to this script file)
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir.parent / "data" / "Valve_list.xlsx"
    df = pd.read_excel(file_path)

    #clean the tag data

    df['VALVE TAG'] = df['VALVE TAG'].astype(str).str.strip()

    # PREFIX EXTRACTION
    # Splitting the first part of the tag name
    df['Prefix'] = df['VALVE TAG'].str.split("-").str[0]

    #Detect duplicates in the 'VALVE TAG' column

    duplicate_counts = df['VALVE TAG'].value_counts()
    duplicates = duplicate_counts[duplicate_counts > 1]

    #  count common prefix
    common_prefix = df['Prefix'].mode()[0] if not df['Prefix'].mode().empty else None
    print(f"Most common prefix: {common_prefix}") 

    # inconsistent prefix detection
    inconsistent_prefixes = df[df['Prefix'] != common_prefix]
    inconsistent_prefixes = inconsistent_prefixes['Prefix'].value_counts()
    # print("\nInconsistent prefixes:")
    # if not inconsistent_prefixes.empty:
    #     for prefix, count in inconsistent_prefixes.items():
    #         print(f"Prefix '{prefix}': {count} occurrences")
    # else:    print("No inconsistent prefixes found.")

    # # NUMBERING EXTRACTION
    # splittin the second part
    df['Number'] = df['VALVE TAG'].str.split("-").str[1]

    # convert to number
    # df['Number'] = pd.to_numeric(df['Number'],errors='coerce')
    df['Number'] = pd.to_numeric(df['Number'], errors='coerce')

    # removing invalid entries
    valid_numbers = df.dropna(subset=['Number'])
    valid_numbers['Number'] = valid_numbers['Number'].astype(int)

    # grouping each number by prefix and checking for missing numbers in the sequence
    groups = valid_numbers.groupby('Prefix')

    # optional: print to show groups by prefix and their numbers
    # print("\nGroups by prefix:")
    # for prefix, group in groups:
    #     print(f"Prefix '{prefix}': Numbers {group['Number'].tolist()}")
    # print("\nChecking for missing numbers in sequence by prefix...")


    missing_report = {}

    for prefix, group in groups:
        numbers = group['Number'].sort_values()
        
        # testing
        # for num in numbers:        print(f"Checking prefix '{prefix}': Number {num}")
        # testing
        # for prefix_one, group_one in numbers.groupby('Prefix'):
        #     print(f"Testing prefix '{prefix_one}': Numbers {group_one.tolist()}")
        
        missing = []
        
        for i in range(len(numbers) - 1):
            current = numbers.iloc[i]
            next_num = numbers.iloc[i + 1]
            
            if next_num != current + 1:
                missing.extend(range(current + 1, next_num))
            else:                continue

        if missing:
            missing_report[prefix] = missing
        else:        continue
            
    # print result   print("No missing numbers in sequence found.")
    # print("\nMissing numbers in sequence by prefix:")
    # if missing_report:
    #     for prefix, missing in missing_report.items():
    #         print(f"Prefix '{prefix}': Missing numbers {missing}")
    # else:    print("No missing numbers in sequence found.")

        
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
    # print("=== TAGs VALIDATOR REPORT === \n")

    # DUPLICATES
    # print("Duplicate VALVE TAGs:")
    # if not duplicates.empty:
    #     for tag, count in duplicates.items():
    #         print(f"VALVE TAG '{tag}': {count} occurrences")
    # else:    print("No duplicate VALVE TAGs found.")

    # print("\nInvalid Format VALVE TAGs:")
    # if invalid_format:
    #     for tag in invalid_format:
    #         # print(f"VALVE TAG '{tag}' does not match the required format.")
    # else:    print("All VALVE TAGs match the required format.")


    # save the duplicates to a new Excel file (path resolved relative to this script)
    # output_dir = script_dir.parent / "output"
    # output_dir.mkdir(parents=True, exist_ok=True)
    # output_path = output_dir / "invalid_format_report.xlsx"
    # duplicates.to_excel(output_path, index=True)
    # pd.DataFrame(invalid_format, columns=['Invalid VALVE TAGs']).to_excel(output_path, index=False, startrow=len(duplicates) + 2)
    # # Append invalid format tags below duplicates
    # print(f"\nInvalid Format VALVE TAGs have been saved to '{output_path}'")


    # CREATING A JSON file report
    report = {
        "total_tags": len(df),
        "duplicates": len(duplicates),
        "invalid_format": len(invalid_format),
        "inconsistent_prefix": len(inconsistent_prefixes),
        "missing_numbers": sum(len(v) for v in missing_report.values())
    }

    # print("\n=== SUMMARY ===")
    # using for loop to iterate through the report dictionary and print each key-value pair
    for key, value in report.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    # combine detailed result
    detailed_report = {
        "duplicates": duplicates.to_dict(),
        "invalid_format": invalid_format,
        "inconsistent_prefixes": inconsistent_prefixes.to_dict(),
        "missing_numbers": missing_report
    }
    # save as JSON file
    import json
    output_json_path = script_dir.parent / "output" / "tag_validation_report.json"
    with open(output_json_path, 'w') as json_file:
        json.dump(detailed_report, json_file, indent=4)
    # print(f"\nDetailed report has been saved to '{output_json_path}'")
    return report, detailed_report
    
# if __name__ == "__main__":
#     main()
