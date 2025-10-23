#!/usr/bin/env python3
"""
tsv_to_csv.py - Convert TSV files to CSV format and process CSV files.

Usage examples:
  # Convert a single TSV file to CSV
  python tsv_to_csv.py input.tsv -o output.csv

  # Convert all TSV files in a directory
  python tsv_to_csv.py --dir ./data

  # Process a CSV file (display info)
  python tsv_to_csv.py --process output.csv

  # Convert TSV to CSV and immediately process it
  python tsv_to_csv.py input.tsv -o output.csv --process
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


def convert_tsv_to_csv(tsv_path: Path, csv_path: Path, encoding: str = 'utf-8') -> bool:
    """
    Convert a TSV file to CSV format.

    Args:
        tsv_path: Path to input TSV file
        csv_path: Path to output CSV file
        encoding: File encoding (default: utf-8)

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Converting: {tsv_path} -> {csv_path}")

        # Read TSV file
        with open(tsv_path, 'r', encoding=encoding, newline='') as tsv_file:
            tsv_reader = csv.reader(tsv_file, delimiter='\t')

            # Write CSV file
            with open(csv_path, 'w', encoding=encoding, newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                row_count = 0
                for row in tsv_reader:
                    csv_writer.writerow(row)
                    row_count += 1

        print(f"  ✓ Converted {row_count} rows successfully")
        return True

    except Exception as e:
        print(f"  ✗ Error converting {tsv_path}: {e}", file=sys.stderr)
        return False


def process_csv_file(csv_path: Path, encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    Process and analyze a CSV file.

    Args:
        csv_path: Path to CSV file
        encoding: File encoding (default: utf-8)

    Returns:
        Dictionary with file analysis information
    """
    try:
        print(f"\n=== Processing CSV: {csv_path} ===")

        # Read CSV using pandas for better analysis
        df = pd.read_csv(csv_path, encoding=encoding)

        info = {
            'file': str(csv_path),
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'null_counts': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum()
        }

        # Display information
        print(f"\nFile: {csv_path}")
        print(f"Rows: {info['rows']}")
        print(f"Columns: {info['columns']}")
        print(f"Memory usage: {info['memory_usage'] / 1024:.2f} KB")

        print("\nColumn Information:")
        print("-" * 80)
        print(f"{'Column Name':<40} {'Type':<15} {'Null Count':<10}")
        print("-" * 80)

        for col in df.columns:
            dtype = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            print(f"{col:<40} {dtype:<15} {null_count:<10}")

        # Show first few rows
        print("\nFirst 5 rows preview:")
        print("-" * 80)
        print(df.head().to_string())

        # Basic statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print("\nNumeric column statistics:")
            print("-" * 80)
            print(df[numeric_cols].describe().to_string())

        return info

    except Exception as e:
        print(f"Error processing {csv_path}: {e}", file=sys.stderr)
        return {}


def convert_directory(directory: Path, output_dir: Path = None, encoding: str = 'utf-8') -> List[Path]:
    """
    Convert all TSV files in a directory to CSV format.

    Args:
        directory: Directory containing TSV files
        output_dir: Output directory (default: same as input)
        encoding: File encoding (default: utf-8)

    Returns:
        List of created CSV file paths
    """
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        return []

    if output_dir is None:
        output_dir = directory
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    tsv_files = list(directory.glob('*.tsv')) + list(directory.glob('*.TSV'))

    if not tsv_files:
        print(f"No TSV files found in {directory}")
        return []

    print(f"Found {len(tsv_files)} TSV file(s) in {directory}")

    csv_files = []
    for tsv_file in tsv_files:
        csv_file = output_dir / f"{tsv_file.stem}.csv"
        if convert_tsv_to_csv(tsv_file, csv_file, encoding):
            csv_files.append(csv_file)

    return csv_files


def main():
    parser = argparse.ArgumentParser(
        description='Convert TSV files to CSV format and process CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'input',
        nargs='?',
        type=Path,
        help='Input TSV file to convert'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output CSV file path (default: same name with .csv extension)'
    )

    parser.add_argument(
        '--dir',
        type=Path,
        help='Convert all TSV files in the specified directory'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory for batch conversion (default: same as input)'
    )

    parser.add_argument(
        '--process',
        nargs='?',
        const=True,
        type=str,
        help='Process and analyze CSV file(s). If no argument, process converted file(s)'
    )

    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='File encoding (default: utf-8)'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.input and not args.dir and not args.process:
        parser.print_help()
        sys.exit(1)

    csv_files = []

    # Batch directory conversion
    if args.dir:
        csv_files = convert_directory(args.dir, args.output_dir, args.encoding)
        if not csv_files:
            sys.exit(1)

    # Single file conversion
    elif args.input:
        if not args.input.exists():
            print(f"Error: Input file {args.input} does not exist", file=sys.stderr)
            sys.exit(1)

        output = args.output or args.input.with_suffix('.csv')

        if convert_tsv_to_csv(args.input, output, args.encoding):
            csv_files.append(output)
        else:
            sys.exit(1)

    # Process CSV files
    if args.process:
        # If process is a string (file path), process that specific file
        if isinstance(args.process, str) and args.process != True:
            process_csv_file(Path(args.process), args.encoding)
        # Otherwise, process the converted files
        elif csv_files:
            for csv_file in csv_files:
                process_csv_file(csv_file, args.encoding)
        else:
            print("Error: No CSV files to process", file=sys.stderr)
            sys.exit(1)

    print("\n✓ Done!")


if __name__ == '__main__':
    main()
