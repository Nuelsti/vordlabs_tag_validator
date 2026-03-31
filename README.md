Vordlabs Tag Validator

# VordLabs Tag Validator

A Streamlit web application that validates valve tag naming conventions in Excel files.

## Features

- Upload multiple Excel files
- Validate tags against naming pattern (`XX-###` or `XXX-###`)
- Detect duplicate tags
- Identify inconsistent prefixes
- Find missing numbers in sequences
- Display detailed validation reports

## Setup

### 1. Create and activate a virtual environment (optional)

**Windows (PowerShell):**
```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

From the project root directory:

```powershell
cd vordlabs-tag-validator
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. Upload one or more Excel files (`.xlsx` format)
2. Click the "Run Validator" button
3. View the validation results including:
   - **Summary Report**: Total tags, duplicates, invalid formats, inconsistent prefixes, missing numbers
   - **Detailed Issues**: Lists of problematic tags with specific violations

## Project Structure

```
vordlabs-tag-validator/
├── app.py                      # Streamlit web application
├── main.py                     # Command-line entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── src/
│   ├── tag_validator.py       # Original validator
│   └── tag_validator_new.py   # Enhanced validator
├── data/                       # Input Excel files
└── output/                     # Generated JSON reports
```

## Tag Naming Convention

Valid tag format: `XX-###` or `XXX-###`
- 2-3 uppercase letters (prefix)
- Hyphen separator
- 3 digits (number)

**Examples:**
- ✅ `AB-001`
- ✅ `ABC-042`
- ❌ `AB-1` (missing digits)
- ❌ `ab-001` (lowercase)

## Output

Validation results are saved to `output/` folder as JSON files with the following structure:

```json
{
  "summary": {
    "total_tags": 50,
    "duplicate_tags": 2,
    "invalid_format_tags": 1,
    "inconsistent_prefixes": 1,
    "missing_numbers": 3
  },
  "details": {
    "duplicates": {...},
    "invalid_format_tags": [...],
    "inconsistent_prefixes": {...},
    "missing_numbers": {...}
  }
}
```

