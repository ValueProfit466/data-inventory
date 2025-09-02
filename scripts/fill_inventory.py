#!/usr/bin/env python3
"""
fill_inventory.py — Guided CLI to complete missing fields in Data_Inventory sheet.
- Validates enums and basic formats (email, URL, dates)
- Offers bulk-fill per column
- Computes quality_total (sum of quality_* 0–3)
- Writes an updated workbook next to the original (suffix _filled.xlsx)
"""
import argparse, re, sys
from pathlib import Path
from urllib.parse import urlparse
import pandas as pd
import yaml

ENUM_COLUMNS = {
    "source_type (official/sector/commercial)": ["official", "sector", "commercial"],
    "license (open/CC-BY/restricted/NDA)": ["open","CC-BY","restricted","NDA"],
    "domain (economisch/vloot/operationeel/milieu/arbeidsmarkt/digitalisering)": [
        "economisch","vloot","operationeel","milieu","arbeidsmarkt","digitalisering"
    ],
    "geographic_coverage (BE/VL/WAL/BXL/EU/CCNR/Corridor)": [
        "BE","VL","WAL","BXL","EU","CCNR","Corridor"
    ],
    "update_frequency (realtime/daily/weekly/monthly/quarterly/annual/ad-hoc)": [
        "realtime","daily","weekly","monthly","quarterly","annual","ad-hoc"
    ],
    "data_status (Volledig/Moet aangevraagd/Ontbreekt/Moet gevalideerd)": [
        "Volledig","Moet aangevraagd","Ontbreekt","Moet gevalideerd"
    ],
    "privacy_sensitivity (low/medium/high)": ["low","medium","high"],
    "contractual_requirements (NDA/DUA/MoU/licence)": ["NDA","DUA","MoU","licence"],
    "priority (A/B/C)": ["A","B","C"]
}

QUALITY_COLUMNS = [
    "quality_completeness (0-3)",
    "quality_accuracy (0-3)",
    "quality_consistency (0-3)",
    "quality_comparability (0-3)",
    "quality_granularity (0-3)",
    "quality_timeliness (0-3)",
    "quality_accessibility (0-3)",
]

REQ_COLUMNS = [
    "source_id","source_name","owner_org","contact_email","url_or_access_method",
    "domain (economisch/vloot/operationeel/milieu/arbeidsmarkt/digitalisering)",
    "dataset_title","geographic_coverage (BE/VL/WAL/BXL/EU/CCNR/Corridor)",
    "update_frequency (realtime/daily/weekly/monthly/quarterly/annual/ad-hoc)",
]

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\\.[^@\\s]+$")
DATE_RE = re.compile(r"^\\d{4}(-\\d{2}(-\\d{2})?)?$")  # YYYY or YYYY-MM or YYYY-MM-DD

def guess_source_type(url: str) -> str | None:
    try:
        host = urlparse(url).hostname or ""
    except Exception:
        return None
    host = host.lower()
    if any(k in host for k in ["statbel","bestat","economie.fgov","eurostat","oecd","worldbank","data.gov"]):
        return "official"
    if any(k in host for k in ["itb","sector","binnenvaart","inlandwaterway","barge","rederij","bevrachting"]):
        return "sector"
    return None

def coerce_enum(value, allowed):
    if pd.isna(value) or value == "":
        return None
    s = str(value).strip()
    for opt in allowed:
        if s.lower() == opt.lower():
            return opt
    return None

def input_enum(prompt, allowed):
    while True:
        val = input(f"{prompt} {allowed} > ").strip()
        if val == "": 
            return None
        coerced = coerce_enum(val, allowed)
        if coerced is not None:
            return coerced
        print(f"Value must be one of {allowed}. Try again.")

def input_text(prompt, validator=None, hint=None):
    while True:
        val = input(f"{prompt}{' ['+hint+']' if hint else ''} > ").strip()
        if val == "":
            return None
        if validator is None or validator(val):
            return val
        print("Invalid value. Try again.")

def is_email(s:str)->bool: return EMAIL_RE.match(s) is not None
def is_date(s:str)->bool: return DATE_RE.match(s) is not None
def is_url(s:str)->bool:
    try:
        p = urlparse(s)
        return p.scheme in ("http","https") and bool(p.netloc)
    except Exception:
        return False

def compute_quality_total(row: pd.Series) -> int:
    total = 0
    for c in QUALITY_COLUMNS:
        try:
            v = int(row.get(c,0)) if pd.notna(row.get(c)) else 0
            if 0 <= v <= 3:
                total += v
        except Exception:
            pass
    return total

def bulk_fill(df: pd.DataFrame, col: str):
    print(f"\\nBulk-fill column: {col}")
    if col in ENUM_COLUMNS:
        val = input_enum(f"Set a single value for all empty cells in '{col}':", ENUM_COLUMNS[col])
    elif col in QUALITY_COLUMNS:
        def qv(x):
            try:
                v=int(x); return 0<=v<=3
            except: return False
        val = input_text(f"Set a single 0-3 value for all empty cells in '{col}':", qv, "0-3")
        val = int(val) if val is not None else None
    elif "email" in col:
        val = input_text(f"Set an email for all empty cells in '{col}':", is_email, "name@org.be")
    elif "date" in col or "time_coverage" in col or "status_last_updated" in col:
        val = input_text(f"Set a date for all empty cells in '{col}':", is_date, "YYYY or YYYY-MM or YYYY-MM-DD")
    elif "url" in col:
        val = input_text(f"Set a URL for all empty cells in '{col}':", is_url, "https://...")
    else:
        val = input_text(f"Set a text for all empty cells in '{col}':")
    if val is not None:
        df.loc[df[col].isna() | (df[col]==""), col] = val

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-xlsx", required=True, help="Path to ITB_data_inventory.xlsx")
    ap.add_argument("--sheet", default="Data_Inventory")
    ap.add_argument("--out-xlsx", help="Output path (default: <in>_filled.xlsx)")
    ap.add_argument("--no-cli", action="store_true", help="Run validations, enrich, and write output without interactive prompts")
    args = ap.parse_args()

    in_path = Path(args.in_xlsx)
    out_path = Path(args.out_xlsx) if args.out_xlsx else in_path.with_name(in_path.stem + "_filled.xlsx")

    xls = pd.ExcelFile(in_path)
    if args.sheet not in xls.sheet_names:
        print(f"Sheet '{args.sheet}' not found. Available: {xls.sheet_names}", file=sys.stderr)
        sys.exit(2)
    df = xls.parse(args.sheet)

    # Standardize empty strings to NaN
    df = df.applymap(lambda x: (None if (isinstance(x,str) and x.strip()=="") else x))

    # Enum coercion + soft guesses
    for col, allowed in ENUM_COLUMNS.items():
        if col in df.columns:
            df[col] = df[col].apply(lambda v: coerce_enum(v, allowed) if pd.notna(v) else v)

    # Guess source_type from URL if missing
    if "source_type (official/sector/commercial)" in df.columns and "url_or_access_method" in df.columns:
        mask = df["source_type (official/sector/commercial)"].isna()
        df.loc[mask, "source_type (official/sector/commercial)"] = df.loc[mask, "url_or_access_method"].apply(guess_source_type)

    # Compute quality_total
    if all(c in df.columns for c in QUALITY_COLUMNS):
        df["quality_total (0-21)"] = df.apply(compute_quality_total, axis=1)

    # Validate required columns
    present_req = [c for c in REQ_COLUMNS if c in df.columns]
    # warn if some expected columns are absent but do not abort
    missing_req = [c for c in REQ_COLUMNS if c not in df.columns]
    if missing_req:
        print("WARN: Missing expected columns:", missing_req, file=sys.stderr)

    # Quick diagnostics
    print("\\n=== Diagnostics ===")
    for c in [c for c in REQ_COLUMNS if c in df.columns]:
        nnull = df[c].isna().sum()
        print(f"{c}: {nnull} empty")

    # Interactive filling loop
    if not args.no_cli:
        while True:
            # Show columns with missing values
            null_counts = df.isna().sum().sort_values(ascending=False)
            todo = [c for c in null_counts.index if null_counts[c] > 0]
            if not todo:
                print("\\nAll fields are filled (no NaNs).")
                break
            print("\\nColumns with missing values (descending):")
            for i, c in enumerate(todo[:20], 1):
                print(f"{i:2d}. {c}  —  {null_counts[c]} missing")
            print("b. Bulk-fill a column  |  e. Edit row-by-row  |  q. Write & quit")
            choice = input("> ").strip().lower()
            if choice == "q":
                break
            elif choice == "b":
                idx = input("Select column number to bulk-fill: ").strip()
                try:
                    k = int(idx)-1
                    if 0 <= k < len(todo[:20]):
                        col = todo[k]
                        bulk_fill(df, col)
                    else:
                        print("Out of range.")
                except ValueError:
                    print("Enter a number.")
            elif choice == "e":
                # row-wise editor: show first row with missing
                row_idx = int(input("Row index to edit (0-based): ").strip())
                if not (0 <= row_idx < len(df)):
                    print("Out of range.")
                    continue
                row = df.loc[row_idx]
                print(f"\\nEditing row {row_idx}:")
                for c in df.columns:
                    cur = row.get(c, None)
                    if pd.isna(cur): cur = ""
                    print(f"- {c}: {cur}")
                    ans = input("  New value (Enter=skip): ").strip()
                    if ans != "":
                        if c in ENUM_COLUMNS:
                            ok = coerce_enum(ans, ENUM_COLUMNS[c])
                            if ok is None:
                                print(f"  Invalid (allowed {ENUM_COLUMNS[c]}), skipping.")
                            else:
                                df.at[row_idx, c] = ok
                        elif "email" in c and not is_email(ans):
                            print("  Invalid email, skipping.")
                        elif ("date" in c or "time_coverage" in c or "status_last_updated" in c) and not is_date(ans):
                            print("  Invalid date, use YYYY or YYYY-MM or YYYY-MM-DD.")
                        elif "url" in c and not is_url(ans):
                            print("  Invalid URL, must start with http(s)://")
                        else:
                            df.at[row_idx, c] = ans
                # recompute quality_total for this row
                if "quality_total (0-21)" in df.columns:
                    df.at[row_idx, "quality_total (0-21)"] = compute_quality_total(df.loc[row_idx])

            else:
                print("Unknown option.")
    # Write output, preserving other sheets
    with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
        # Write original sheets
        for name in xls.sheet_names:
            if name == args.sheet:
                continue
            xls.parse(name).to_excel(writer, sheet_name=name, index=False)
        # Write updated inventory
        df.to_excel(writer, sheet_name=args.sheet, index=False)
    print(f"\\nSaved: {out_path}")
if __name__ == "__main__":
    main()
