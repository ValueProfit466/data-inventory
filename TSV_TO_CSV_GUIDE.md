# TSV to CSV Conversion Guide

## Overview

This guide shows you how to use the `tsv_to_csv.py` script to convert Tab-Separated Values (TSV) files to Comma-Separated Values (CSV) format and process the resulting CSV files.

## Installation

First, ensure pandas is installed:

```bash
pip install pandas
```

## Usage Examples

### 1. Convert a Single TSV File to CSV

```bash
python scripts/tsv_to_csv.py input.tsv
```

This creates `input.csv` in the same directory.

### 2. Specify Output Location

```bash
python scripts/tsv_to_csv.py input.tsv -o output/data.csv
```

### 3. Convert and Immediately Process

```bash
python scripts/tsv_to_csv.py samples/example_data.tsv --process
```

This converts the TSV to CSV and displays:
- Number of rows and columns
- Column data types
- Null value counts
- First 5 rows preview
- Statistics for numeric columns

### 4. Convert All TSV Files in a Directory

```bash
python scripts/tsv_to_csv.py --dir ./data
```

### 5. Process an Existing CSV File

```bash
python scripts/tsv_to_csv.py --process data.csv
```

## Script Features

### Conversion Features
- Converts TSV (tab-delimited) files to CSV (comma-delimited) format
- Handles various text encodings (default: UTF-8)
- Preserves all data integrity during conversion
- Batch processing for multiple files

### Processing Features
When using `--process`, the script provides:
- **Row and column counts**
- **Column information**: name, data type, null count
- **Data preview**: First 5 rows
- **Statistics**: For numeric columns (mean, std, min, max, quartiles)
- **Memory usage**: File size analysis

## Example Output

```
Converting: samples/example_data.tsv -> samples/example_data.csv
  ✓ Converted 5 rows successfully

=== Processing CSV: samples/example_data.csv ===

File: samples/example_data.csv
Rows: 4
Columns: 9
Memory usage: 2.37 KB

Column Information:
--------------------------------------------------------------------------------
Column Name                              Type            Null Count
--------------------------------------------------------------------------------
source_id                                int64           0
source_name                              object          0
owner_org                                object          0
...
```

## Processing CSV Files in Python

You can also import and use the conversion functions in your own Python code:

```python
from pathlib import Path
from scripts.tsv_to_csv import convert_tsv_to_csv, process_csv_file

# Convert a file
convert_tsv_to_csv(
    Path('input.tsv'),
    Path('output.csv')
)

# Process and analyze
info = process_csv_file(Path('output.csv'))
print(f"Total rows: {info['rows']}")
```

## Using CSV Files with Pandas

Once converted to CSV, you can easily work with the data using pandas:

```python
import pandas as pd

# Read the CSV
df = pd.read_csv('samples/example_data.csv')

# Basic operations
print(df.head())                    # View first rows
print(df.describe())                # Statistics
print(df['column_name'].value_counts())  # Count values

# Filter data
filtered = df[df['source_id'] > 1]

# Export to other formats
df.to_excel('output.xlsx', index=False)
df.to_json('output.json', orient='records')
```

## Command-Line Options

```
usage: tsv_to_csv.py [-h] [-o OUTPUT] [--dir DIR] [--output-dir OUTPUT_DIR]
                     [--process [PROCESS]] [--encoding ENCODING] [input]

Options:
  input                 Input TSV file to convert
  -o, --output         Output CSV file path
  --dir                Convert all TSV files in directory
  --output-dir         Output directory for batch conversion
  --process            Process and analyze CSV file(s)
  --encoding           File encoding (default: utf-8)
  -h, --help           Show help message
```

## Example Workflow

1. **Place your TSV files** in the project (e.g., in `samples/` or `data/`)

2. **Convert to CSV**:
   ```bash
   python scripts/tsv_to_csv.py my_data.tsv
   ```

3. **Analyze the data**:
   ```bash
   python scripts/tsv_to_csv.py --process my_data.csv
   ```

4. **Process with pandas**:
   ```python
   import pandas as pd
   df = pd.read_csv('my_data.csv')
   # Your analysis here
   ```

## Try It Now!

An example TSV file is included in `samples/example_data.tsv`. Try converting it:

```bash
python scripts/tsv_to_csv.py samples/example_data.tsv --process
```

## Notes

- The script preserves the original TSV files (they are not deleted)
- CSV files use UTF-8 encoding by default
- Large files are handled efficiently using streaming
- For integration with the existing inventory system, CSV files can be imported into Excel or processed with the `fill_inventory.py` script
