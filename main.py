import argparse
import pandas as pd
import os
import json
from src.tag_validator_new import run_validator

def main():
    parser = argparse.ArgumentParser(description='Process valve tag data.')
    parser.add_argument(
        '--file', 
        type=str, 
        required=True, 
        help='Path to the input Excel file containing valve tag data.'
    )
    parser.add_argument(
        '--output',
        type=str,
        # required=True,
        default='output/tag_validation_new_report.json',
        help='Path to the output JSON file for the validation report.'
    )
    args = parser.parse_args()
    # Resolve the path to the input file
    file_path = args.file
    # Resolve the path to the output file
    output_path = args.output
    # Run the validator
    report, detailed_report = run_validator(file_path, output_path)
    print("Validation report generated successfully.")
    print(json.dumps(report, indent=4))
    
if __name__ == "__main__":
    main()
   


