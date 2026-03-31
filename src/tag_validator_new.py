from pathlib import Path
import pandas as pd
import sys
import os
import re
import json

def run_validator(file_path, output_path):
    # ensure output folder exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # load data
    df = pd.read_excel(file_path)
    #clean the tag data
    # inform user about the cleaning process and how the valve tag header is structured
    df['VALVE TAG'] = df['VALVE TAG'].astype(str).str.strip()
    
    # DUPLICATE DETECTION
    duplicate_counts = df['VALVE TAG'].value_counts()
    duplicates = duplicate_counts[duplicate_counts > 1]
    
    # FORMAT VALIDATION
    pattern = r'^[A-Z]{2,3}-\d{3}$'
    invalid_format = []
    for tag in df['VALVE TAG']:
        if pd.isna(tag):
            continue
        t = str(tag).strip()
        if not re.match(pattern, t):
            invalid_format.append(t)
    
    # PREFIX EXTRACTION
    df['Prefix'] = df['VALVE TAG'].str.split("-").str[0]
    
    # CONSISTENCY CHECK
    common_prefix = df['Prefix'].mode()[0] if not df['Prefix'].mode().empty else None
    inconsistent_prefixes = df[df['Prefix'] != common_prefix]
    
    # NUMBERING EXTRACTION
    df['Number'] = df['VALVE TAG'].str.split("-").str[1]
    df['Number'] = pd.to_numeric(df['Number'], errors='coerce')
    valid_numbers = df.dropna(subset=['Number']).copy()
    valid_numbers['Number'] = valid_numbers['Number'].astype(int)
    
    # MISSING NUMBER DETECTION
    groups = valid_numbers.groupby('Prefix')
    
    missing_report = {}
    for prefix, group in groups:
        numbers = sorted(group['Number'].tolist())
        if not numbers:
            continue
        min_num, max_num = numbers[0], numbers[-1]
        full_set = set(range(min_num, max_num + 1))
        missing_numbers = sorted(full_set - set(numbers))
        if missing_numbers:
            missing_report[prefix] = missing_numbers
    
    # COMPILE REPORT
    report = {
        "total_tags": len(df),
        "duplicate_tags": len(duplicates),
        "invalid_format_tags": len(invalid_format),
        "inconsistent_prefixes": inconsistent_prefixes['Prefix'].nunique(),
        "missing_numbers": sum(len(v) for v in missing_report.values())
    }
    detailed_report = {
        "duplicates": duplicates.to_dict(),
        "invalid_format_tags": invalid_format,
        "inconsistent_prefixes": inconsistent_prefixes['Prefix'].value_counts().to_dict(),
        "missing_numbers": missing_report   
    }
    final_report = {
        "summary": report,
        "details": detailed_report
    }
    
    # Save the detailed report to a JSON file
    with open(output_path, 'w') as json_file:
        json.dump(final_report, json_file, indent=4)
    
    return final_report

    

    
