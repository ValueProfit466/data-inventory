#!/usr/bin/env python3
"""
clean_eurostat.py - Clean, filter, and analyze Eurostat transport data

Features:
- Parse Eurostat metadata (freq, unit, tra_mode, geo)
- Clean values (remove flags: e, b, p, n, m, etc.)
- Geographic filtering (select specific countries)
- Transport mode filtering
- Reshape data (wide to long format)
- Export cleaned data to CSV/Excel
- Generate summary statistics
"""

import argparse
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
import pandas as pd


class EurostatCleaner:
    """Clean and process Eurostat transport data"""

    # Eurostat data flags
    FLAGS = {
        'e': 'estimated',
        'p': 'provisional',
        'b': 'break in time series',
        'n': 'not significant',
        'c': 'confidential',
        'd': 'definition differs',
        'u': 'low reliability',
        's': 'Eurostat estimate',
        'i': 'see metadata',
        'r': 'revised',
        'z': 'not applicable',
        ':': 'not available',
        'm': 'missing'
    }

    def __init__(self, csv_path: Path):
        """Initialize with path to converted CSV file"""
        self.csv_path = csv_path
        self.df = None
        self.metadata_col = None
        self.year_cols = None
        self.cleaned_df = None
        self.long_df = None

    def load_data(self):
        """Load the Eurostat CSV file"""
        print(f"Loading data from: {self.csv_path}")
        self.df = pd.read_csv(self.csv_path)
        self.metadata_col = self.df.columns[0]
        # Store cleaned year column names
        self.year_cols = [col.strip() for col in self.df.columns[1:]]
        print(f"  Loaded {len(self.df)} rows, {len(self.year_cols)} years ({self.year_cols[0]}-{self.year_cols[-1]})")

    def parse_metadata(self) -> pd.DataFrame:
        """Parse metadata column into separate fields"""
        print("\nParsing metadata...")

        parsed = []
        for idx, row in self.df.iterrows():
            meta_str = row[self.metadata_col]
            parts = meta_str.split(',')

            if len(parts) >= 4:
                parsed.append({
                    'row_idx': idx,
                    'freq': parts[0].strip(),
                    'unit': parts[1].strip(),
                    'tra_mode': parts[2].strip(),
                    'geo': parts[3].strip()
                })

        meta_df = pd.DataFrame(parsed)
        print(f"  Parsed metadata for {len(meta_df)} rows")
        return meta_df

    def clean_value(self, value: Any) -> Optional[float]:
        """
        Clean a single value by removing Eurostat flags

        Returns:
            float: Cleaned numeric value
            None: If value is missing/not available
        """
        if pd.isna(value):
            return None

        value_str = str(value).strip()

        # Handle missing values
        if value_str in ['', ':', ': m', ': c', ': z']:
            return None

        # Remove all letter flags and extra spaces
        cleaned = re.sub(r'[a-zA-Z :]+', '', value_str)

        # Try to convert to float
        try:
            return float(cleaned) if cleaned else None
        except ValueError:
            return None

    def extract_flags(self, value: Any) -> List[str]:
        """Extract all flags from a value"""
        if pd.isna(value):
            return []

        value_str = str(value).strip()
        flags = re.findall(r'[a-z]', value_str)
        return flags

    def clean_data(self) -> pd.DataFrame:
        """Clean all numeric values and create cleaned dataframe"""
        print("\nCleaning data values...")

        meta_df = self.parse_metadata()

        # Create cleaned dataframe with metadata
        cleaned = meta_df.copy()

        # Clean year columns - handle both original and stripped names
        for year_col in self.df.columns[1:]:
            year_clean = year_col.strip()
            cleaned[year_clean] = self.df[year_col].apply(self.clean_value)

        self.cleaned_df = cleaned

        # Calculate statistics
        total_cells = len(cleaned) * len(self.year_cols)
        non_null = cleaned[self.year_cols].notna().sum().sum()
        pct_complete = (non_null / total_cells) * 100

        print(f"  Cleaned {total_cells} cells")
        print(f"  Valid values: {non_null} ({pct_complete:.1f}%)")

        return cleaned

    def filter_geo(self, countries: List[str]) -> 'EurostatCleaner':
        """Filter data to specific countries"""
        if self.cleaned_df is None:
            raise ValueError("Must clean data first (call clean_data())")

        print(f"\nFiltering to countries: {', '.join(countries)}")

        # Case-insensitive matching
        countries_upper = [c.upper() for c in countries]
        mask = self.cleaned_df['geo'].str.upper().isin(countries_upper)

        self.cleaned_df = self.cleaned_df[mask].copy()
        print(f"  Retained {len(self.cleaned_df)} rows")

        return self

    def filter_mode(self, modes: List[str]) -> 'EurostatCleaner':
        """Filter data to specific transport modes"""
        if self.cleaned_df is None:
            raise ValueError("Must clean data first (call clean_data())")

        print(f"\nFiltering to transport modes: {', '.join(modes)}")

        modes_upper = [m.upper() for m in modes]
        mask = self.cleaned_df['tra_mode'].str.upper().isin(modes_upper)

        self.cleaned_df = self.cleaned_df[mask].copy()
        print(f"  Retained {len(self.cleaned_df)} rows")

        return self

    def to_long_format(self) -> pd.DataFrame:
        """
        Reshape data from wide to long format

        Wide:  geo | 2020 | 2021 | 2022
        Long:  geo | year | value
        """
        print("\nReshaping to long format...")

        if self.cleaned_df is None:
            raise ValueError("Must clean data first (call clean_data())")

        # Metadata columns
        id_vars = ['freq', 'unit', 'tra_mode', 'geo']

        # Melt the dataframe
        long_df = self.cleaned_df.melt(
            id_vars=id_vars,
            value_vars=self.year_cols,
            var_name='year',
            value_name='value'
        )

        # Convert year to int
        long_df['year'] = long_df['year'].astype(int)

        # Remove rows with null values
        long_df = long_df.dropna(subset=['value'])

        # Sort
        long_df = long_df.sort_values(['geo', 'tra_mode', 'year']).reset_index(drop=True)

        self.long_df = long_df

        print(f"  Created long format with {len(long_df)} rows")
        return long_df

    def summary_stats(self) -> pd.DataFrame:
        """Generate summary statistics"""
        if self.cleaned_df is None:
            raise ValueError("Must clean data first (call clean_data())")

        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)

        # Overall stats
        print(f"\nDataset Overview:")
        print(f"  Countries: {self.cleaned_df['geo'].nunique()}")
        print(f"  Transport modes: {self.cleaned_df['tra_mode'].nunique()}")
        print(f"  Years: {len(self.year_cols)}")

        # By country
        print(f"\nData by Country:")
        country_stats = []
        for geo in sorted(self.cleaned_df['geo'].unique()):
            geo_data = self.cleaned_df[self.cleaned_df['geo'] == geo]
            values = geo_data[self.year_cols].values.flatten()
            values = values[~pd.isna(values)]

            if len(values) > 0:
                country_stats.append({
                    'Country': geo,
                    'Data Points': len(values),
                    'Mean': values.mean(),
                    'Median': pd.Series(values).median(),
                    'Min': values.min(),
                    'Max': values.max()
                })

        stats_df = pd.DataFrame(country_stats)
        print(stats_df.to_string(index=False))

        # By transport mode
        print(f"\nData by Transport Mode:")
        mode_stats = []
        for mode in sorted(self.cleaned_df['tra_mode'].unique()):
            mode_data = self.cleaned_df[self.cleaned_df['tra_mode'] == mode]
            values = mode_data[self.year_cols].values.flatten()
            values = values[~pd.isna(values)]

            if len(values) > 0:
                mode_stats.append({
                    'Transport Mode': mode,
                    'Data Points': len(values),
                    'Mean': values.mean(),
                    'Median': pd.Series(values).median(),
                    'Min': values.min(),
                    'Max': values.max()
                })

        mode_df = pd.DataFrame(mode_stats)
        print(mode_df.to_string(index=False))

        return stats_df

    def analyze_trends(self):
        """Analyze trends over time"""
        if self.cleaned_df is None:
            raise ValueError("Must clean data first (call clean_data())")

        print("\n" + "="*80)
        print("TREND ANALYSIS")
        print("="*80)

        # Year-over-year changes
        print(f"\nYear-over-year statistics:")
        print(f"{'Year':<8} {'Count':>8} {'Mean':>10} {'Median':>10} {'Std Dev':>10}")
        print("-" * 56)

        for year in self.year_cols:
            values = self.cleaned_df[year].dropna()
            if len(values) > 0:
                print(f"{year:<8} {len(values):>8} {values.mean():>10.2f} "
                      f"{values.median():>10.2f} {values.std():>10.2f}")

        # Overall trend
        first_year = self.year_cols[0]
        last_year = self.year_cols[-1]

        first_mean = self.cleaned_df[first_year].mean()
        last_mean = self.cleaned_df[last_year].mean()

        if not pd.isna(first_mean) and not pd.isna(last_mean):
            change = last_mean - first_mean
            pct_change = (change / first_mean) * 100

            print(f"\nOverall Trend ({first_year} to {last_year}):")
            print(f"  {first_year} average: {first_mean:.2f}")
            print(f"  {last_year} average: {last_mean:.2f}")
            print(f"  Change: {change:+.2f} ({pct_change:+.1f}%)")

    def export_wide(self, output_path: Path):
        """Export cleaned data in wide format (countries x years)"""
        if self.cleaned_df is None:
            raise ValueError("Must clean data first (call clean_data())")

        print(f"\nExporting wide format to: {output_path}")

        if output_path.suffix == '.xlsx':
            self.cleaned_df.to_excel(output_path, index=False)
        else:
            self.cleaned_df.to_csv(output_path, index=False)

        print(f"  ✓ Exported {len(self.cleaned_df)} rows")

    def export_long(self, output_path: Path):
        """Export cleaned data in long format (one row per observation)"""
        if self.long_df is None:
            self.to_long_format()

        print(f"\nExporting long format to: {output_path}")

        if output_path.suffix == '.xlsx':
            self.long_df.to_excel(output_path, index=False)
        else:
            self.long_df.to_csv(output_path, index=False)

        print(f"  ✓ Exported {len(self.long_df)} rows")


def main():
    parser = argparse.ArgumentParser(
        description='Clean and filter Eurostat transport data',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'input',
        type=Path,
        help='Input CSV file (converted from TSV)'
    )

    parser.add_argument(
        '-g', '--geo',
        nargs='+',
        help='Filter to specific countries (e.g., BE NL DE FR)'
    )

    parser.add_argument(
        '-m', '--mode',
        nargs='+',
        choices=['IWW', 'RAIL', 'ROAD', 'RAIL_IWW_AVD'],
        help='Filter to specific transport modes'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file for cleaned data (CSV or XLSX)'
    )

    parser.add_argument(
        '--long',
        action='store_true',
        help='Export in long format (one row per observation)'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show summary statistics'
    )

    parser.add_argument(
        '--trends',
        action='store_true',
        help='Show trend analysis'
    )

    args = parser.parse_args()

    # Validate input
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    # Initialize cleaner
    cleaner = EurostatCleaner(args.input)

    # Load and clean
    cleaner.load_data()
    cleaner.clean_data()

    # Apply filters
    if args.geo:
        cleaner.filter_geo(args.geo)

    if args.mode:
        cleaner.filter_mode(args.mode)

    # Analysis
    if args.stats:
        cleaner.summary_stats()

    if args.trends:
        cleaner.analyze_trends()

    # Export
    if args.output:
        if args.long:
            cleaner.export_long(args.output)
        else:
            cleaner.export_wide(args.output)

    print("\n✓ Done!")
    return 0


if __name__ == '__main__':
    exit(main())
