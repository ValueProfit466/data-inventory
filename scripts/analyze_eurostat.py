#!/usr/bin/env python3
"""
analyze_eurostat.py - Detailed analysis of Eurostat transport data
"""
import pandas as pd
import re
from pathlib import Path


def parse_eurostat_header(header_str):
    """Parse the Eurostat metadata column (freq,unit,tra_mode,geo\\TIME_PERIOD)"""
    parts = header_str.split(',')
    if len(parts) == 4:
        freq, unit, tra_mode, geo = parts
        geo = geo.split('\\')[0]  # Remove TIME_PERIOD suffix
        return {'freq': freq, 'unit': unit, 'tra_mode': tra_mode, 'geo': geo}
    return None


def clean_eurostat_value(value):
    """Remove Eurostat flags (e, b, p, etc.) and convert to float"""
    if pd.isna(value) or value.strip() == '' or ':' in value:
        return None

    # Remove common Eurostat flags
    cleaned = re.sub(r'[a-z :]+', '', str(value).strip())
    try:
        return float(cleaned)
    except ValueError:
        return None


def analyze_eurostat_file(csv_path):
    """Comprehensive analysis of Eurostat transport data"""

    print(f"\n{'='*80}")
    print(f"EUROSTAT TRANSPORT DATA ANALYSIS: {csv_path.name}")
    print(f"{'='*80}\n")

    # Read the CSV
    df = pd.read_csv(csv_path)

    # Parse metadata column
    metadata_col = df.columns[0]
    year_cols = df.columns[1:]

    print(f"Dataset Structure:")
    print(f"  Total rows: {len(df)}")
    print(f"  Metadata column: '{metadata_col}'")
    print(f"  Year columns: {len(year_cols)} years ({year_cols[0]} to {year_cols[-1]})")

    # Parse metadata for each row
    print(f"\n{'='*80}")
    print("METADATA BREAKDOWN")
    print(f"{'='*80}\n")

    parsed_data = []
    for idx, row in df.iterrows():
        meta_str = row[metadata_col]
        parts = meta_str.split(',')
        if len(parts) >= 4:
            parsed_data.append({
                'freq': parts[0],
                'unit': parts[1],
                'tra_mode': parts[2],
                'geo': parts[3]
            })

    meta_df = pd.DataFrame(parsed_data)

    print("Frequency (freq):")
    print(meta_df['freq'].value_counts().to_string())

    print("\nUnit (unit):")
    print(meta_df['unit'].value_counts().to_string())

    print("\nTransport Mode (tra_mode):")
    print(meta_df['tra_mode'].value_counts().to_string())

    print("\nGeographic Coverage (geo):")
    geo_counts = meta_df['geo'].value_counts()
    print(f"  Total countries/regions: {len(geo_counts)}")
    print(f"  Countries: {', '.join(sorted(geo_counts.index.tolist()))}")

    # Analyze data quality
    print(f"\n{'='*80}")
    print("DATA QUALITY ANALYSIS")
    print(f"{'='*80}\n")

    # Count missing values, estimated values, breaks in series
    missing_count = 0
    estimated_count = 0
    break_count = 0
    valid_count = 0

    for col in year_cols:
        for val in df[col]:
            val_str = str(val).strip()
            if ':' in val_str or val_str == 'nan' or val_str == '':
                missing_count += 1
            elif 'e' in val_str:
                estimated_count += 1
                valid_count += 1
            elif 'b' in val_str:
                break_count += 1
                valid_count += 1
            else:
                valid_count += 1

    total_cells = len(df) * len(year_cols)

    print(f"Total data cells: {total_cells}")
    print(f"  Valid values: {valid_count} ({valid_count/total_cells*100:.1f}%)")
    print(f"  Missing/Not available: {missing_count} ({missing_count/total_cells*100:.1f}%)")
    print(f"  Estimated (e): {estimated_count} ({estimated_count/total_cells*100:.1f}%)")
    print(f"  Break in series (b): {break_count} ({break_count/total_cells*100:.1f}%)")

    # Sample data by country
    print(f"\n{'='*80}")
    print("SAMPLE DATA BY COUNTRY (First 10 countries)")
    print(f"{'='*80}\n")

    for idx in range(min(10, len(df))):
        row = df.iloc[idx]
        meta = row[metadata_col]
        country = meta.split(',')[-1] if ',' in meta else 'Unknown'

        # Show last 3 years
        recent_years = year_cols[-3:]
        recent_values = [row[year] for year in recent_years]

        print(f"{country:4s}: ", end='')
        for year, val in zip(recent_years, recent_values):
            print(f"{year}={val:>8s}", end='  ')
        print()

    # Create cleaned numeric dataset
    print(f"\n{'='*80}")
    print("NUMERIC STATISTICS (Cleaned Data)")
    print(f"{'='*80}\n")

    numeric_df = df[year_cols].applymap(clean_eurostat_value)

    print("Year-by-year statistics:")
    print(f"{'Year':<8} {'Count':>8} {'Mean':>10} {'Median':>10} {'Min':>10} {'Max':>10}")
    print("-" * 66)

    for year in year_cols:
        values = numeric_df[year].dropna()
        if len(values) > 0:
            print(f"{year:<8} {len(values):>8} {values.mean():>10.2f} "
                  f"{values.median():>10.2f} {values.min():>10.2f} {values.max():>10.2f}")

    # Trend analysis
    print(f"\n{'='*80}")
    print("TREND ANALYSIS")
    print(f"{'='*80}\n")

    # Compare first and last available years
    first_year_values = numeric_df[year_cols[0]].dropna()
    last_year_values = numeric_df[year_cols[-1]].dropna()

    if len(first_year_values) > 0 and len(last_year_values) > 0:
        print(f"Average in {year_cols[0]}: {first_year_values.mean():.2f}")
        print(f"Average in {year_cols[-1]}: {last_year_values.mean():.2f}")
        change = last_year_values.mean() - first_year_values.mean()
        pct_change = (change / first_year_values.mean()) * 100
        print(f"Change: {change:+.2f} ({pct_change:+.1f}%)")

    return df, meta_df, numeric_df


if __name__ == '__main__':
    csv_path = Path('samples/estat_tran_hv_frmod.csv')

    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        print("Please run: python scripts/tsv_to_csv.py samples/estat_tran_hv_frmod.tsv")
        exit(1)

    df, meta_df, numeric_df = analyze_eurostat_file(csv_path)

    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print("\nDataFrames available for further analysis:")
    print("  df         - Original data")
    print("  meta_df    - Parsed metadata")
    print("  numeric_df - Cleaned numeric values")
