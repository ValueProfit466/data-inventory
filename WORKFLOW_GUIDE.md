# Complete Data Processing & Inventory Workflow

This guide shows the **end-to-end workflow** for processing external data sources and adding them to your simplified inventory system.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Step-by-Step Workflow](#step-by-step-workflow)
3. [Tools Overview](#tools-overview)
4. [Simplified Inventory Schema](#simplified-inventory-schema)
5. [Example: Eurostat Data Processing](#example-eurostat-data-processing)
6. [Command Reference](#command-reference)

---

## 🚀 Quick Start

```bash
# 1. Convert TSV to CSV
python scripts/tsv_to_csv.py data.tsv

# 2. Clean and filter the data
python scripts/clean_eurostat.py data.csv --geo BE NL --stats --output cleaned.csv

# 3. Add to inventory
python scripts/simple_inventory.py --inventory data_inventory_simple.csv add --interactive
```

---

## 📖 Step-by-Step Workflow

### Step 1: Obtain Data

Download or receive data from external source (Eurostat, government portals, APIs, etc.)

```bash
# Example: Download from Eurostat
# (Or receive file via email, FTP, etc.)
```

### Step 2: Convert to CSV (if needed)

If the data is in TSV format:

```bash
python scripts/tsv_to_csv.py samples/estat_tran_hv_frmod.tsv --process
```

**Output:**
- Converted CSV file
- Basic analysis (row/column counts, data types, missing values)

### Step 3: Clean and Filter Data

Use the cleaning tool to:
- Remove Eurostat flags (e, p, b, n, etc.)
- Filter by geography
- Filter by variables/dimensions
- Generate statistics

```bash
python scripts/clean_eurostat.py samples/estat_tran_hv_frmod.csv \
  --geo BE NL DE FR \
  --mode IWW ROAD \
  --stats \
  --trends \
  --output samples/benelux_transport_clean.csv
```

**Output:**
- Cleaned CSV file (numeric values only)
- Summary statistics by country and transport mode
- Trend analysis over time

### Step 4: Analyze Data Quality

Review the output from Step 3:
- **Completeness**: % of non-missing values
- **Countries covered**: Which regions have data
- **Years available**: Time span of data
- **Variables**: What metrics are included

Use this to assess data quality (1-5 stars) for inventory.

### Step 5: Add to Inventory

#### Option A: Interactive Mode (Recommended)

```bash
python scripts/simple_inventory.py --inventory data_inventory_simple.csv add --interactive
```

Follow the prompts to enter all fields.

#### Option B: Command-Line Mode

```bash
python scripts/simple_inventory.py --inventory data_inventory_simple.csv add \
  --source-id ESTAT_HV_001 \
  --topic Transport \
  --name "Eurostat Heavy Vehicle Freight Modal Split" \
  --url "https://ec.europa.eu/eurostat/databrowser/view/tran_hv_frmod/" \
  --file "samples/estat_tran_hv_frmod.csv" \
  --format CSV \
  --years "2005-2023" \
  --geo "EU27, 32 countries"
```

#### Option C: Python Script

Create a script to add complete entry (see `scripts/populate_inventory.py`)

### Step 6: Review and Manage Inventory

```bash
# List all entries
python scripts/simple_inventory.py --inventory data_inventory_simple.csv list

# Show specific entry
python scripts/simple_inventory.py --inventory data_inventory_simple.csv show ESTAT_HV_001

# Search inventory
python scripts/simple_inventory.py --inventory data_inventory_simple.csv search "transport"

# Export template
python scripts/simple_inventory.py template inventory_template.csv
```

---

## 🛠 Tools Overview

### 1. **tsv_to_csv.py** - Format Conversion

**Purpose:** Convert TSV files to CSV and provide basic analysis

**Features:**
- Single file or batch directory conversion
- Data type detection
- Missing value analysis
- Preview of data

**Usage:**
```bash
# Convert single file
python scripts/tsv_to_csv.py input.tsv

# Convert and analyze
python scripts/tsv_to_csv.py input.tsv --process

# Batch convert directory
python scripts/tsv_to_csv.py --dir ./data_folder
```

### 2. **clean_eurostat.py** - Data Cleaning & Filtering

**Purpose:** Clean Eurostat data, remove flags, filter by geography/variables

**Features:**
- Parse Eurostat metadata (freq, unit, tra_mode, geo)
- Clean values (remove flags: e, b, p, n, etc.)
- Geographic filtering
- Transport mode filtering
- Summary statistics
- Trend analysis
- Export wide or long format

**Usage:**
```bash
# Clean and filter
python scripts/clean_eurostat.py data.csv \
  --geo BE NL DE \
  --mode IWW RAIL \
  --stats \
  --output cleaned.csv

# Long format for time-series analysis
python scripts/clean_eurostat.py data.csv \
  --geo BE \
  --long \
  --output belgium_long.csv
```

### 3. **simple_inventory.py** - Inventory Management

**Purpose:** Manage simplified data source inventory

**Features:**
- Add new data sources
- List and filter entries
- Search by keyword
- Show detailed entry information
- Delete entries
- Export templates

**Usage:**
```bash
# Interactive add
python scripts/simple_inventory.py --inventory data_inventory_simple.csv add --interactive

# List all
python scripts/simple_inventory.py --inventory data_inventory_simple.csv list

# Show entry
python scripts/simple_inventory.py --inventory data_inventory_simple.csv show ESTAT_HV_001

# Search
python scripts/simple_inventory.py --inventory data_inventory_simple.csv search "eurostat"
```

---

## 📊 Simplified Inventory Schema

Your new streamlined inventory has **15 fields**:

| Field | Description | Example |
|-------|-------------|---------|
| **Source ID** | Unique identifier | `ESTAT_HV_001` |
| **Topic** | Subject area | `Transport`, `Economics`, `Environment` |
| **Source Name** | Name of data source | `Eurostat Heavy Vehicle Freight Modal Split` |
| **URL** | Web address | `https://ec.europa.eu/eurostat/...` |
| **Date Accessed** | When accessed | `2025-10-23` |
| **Data Years** | Time period covered | `2005-2023 (annual)` |
| **Geographic Scope** | Geographic coverage | `EU27, 32 European countries` |
| **File Location** | Path to local files | `samples/estat_tran_hv_frmod.csv` |
| **Data Format** | File format | `CSV`, `Excel`, `JSON`, `API` |
| **Key Variables** | Main variables | `tra_mode, geo, yearly percentages` |
| **Data Quality** | Quality rating & notes | `⭐⭐⭐⭐⭐ (5/5) - Official data, 86.5% complete` |
| **Limitations** | Known issues | `13.5% missing values, no sub-annual data` |
| **Update Frequency** | How often updated | `Annual`, `Monthly`, `Real-time` |
| **Contact Info** | Contact person/org | `estat-user-support@ec.europa.eu` |
| **Notes** | Additional information | `Belgium: 10-11% IWW usage. Trend: -5.6% decline` |

### Benefits Over Old System

✅ **Simpler** - 15 fields vs 30+ in old system
✅ **Flexible** - Free-text notes instead of rigid enums
✅ **Practical** - Focuses on what you actually need
✅ **Fast** - Quick to add entries
✅ **Searchable** - Easy keyword search
✅ **Portable** - CSV or Excel format

---

## 📌 Example: Eurostat Data Processing

Here's the complete workflow we followed for the Eurostat transport data:

### 1. Received Data
```
File: estat_tran_hv_frmod.tsv
Source: GitHub repository (samples/)
```

### 2. Converted to CSV
```bash
python scripts/tsv_to_csv.py samples/estat_tran_hv_frmod.tsv --process
```

**Results:**
- 128 rows, 20 columns
- 19 years of data (2005-2023)
- 32 countries
- 4 transport modes (IWW, RAIL, ROAD, RAIL_IWW_AVD)

### 3. Cleaned and Filtered

#### Filter for Belgium
```bash
python scripts/clean_eurostat.py samples/estat_tran_hv_frmod.csv \
  --geo BE \
  --stats \
  --trends \
  --output samples/eurostat_belgium_clean.csv
```

**Results:**
- Belgium IWW: 10.7-16.4% modal share
- Declining trend in recent years
- 100% data completeness for Belgium

#### Filter for Benelux
```bash
python scripts/clean_eurostat.py samples/estat_tran_hv_frmod.csv \
  --geo BE NL DE FR \
  --mode IWW \
  --stats \
  --output samples/eurostat_benelux_iww.csv
```

**Results:**
- Belgium: 13.5% average
- Netherlands: 43.5% average (very high!)
- Germany: 9.2% average
- France: 2.6% average

### 4. Long Format for Analysis
```bash
python scripts/clean_eurostat.py samples/estat_tran_hv_frmod.csv \
  --geo BE \
  --long \
  --output samples/eurostat_belgium_long.csv
```

**Results:**
- 76 rows (4 modes × 19 years)
- Ready for time-series analysis
- Easy to plot with pandas/matplotlib

### 5. Added to Inventory
```bash
python scripts/populate_inventory.py
```

**Entry created with:**
- Source ID: `ESTAT_HV_001`
- Data Quality: ⭐⭐⭐⭐⭐ (5/5 stars)
- All fields populated
- Links to cleaned data files
- Key insights in Notes field

### 6. Verified Entry
```bash
python scripts/simple_inventory.py --inventory data_inventory_simple.csv show ESTAT_HV_001
```

**Output:**
```
================================================================================
DATA SOURCE: ESTAT_HV_001
================================================================================

Source ID           : ESTAT_HV_001
Topic               : Transport
Source Name         : Eurostat Heavy Vehicle Freight Modal Split
URL                 : https://ec.europa.eu/eurostat/databrowser/view/tran_hv_frmod/
Date Accessed       : 2025-10-23
Data Years          : 2005-2023 (annual)
Geographic Scope    : EU27, EU28, 32 European countries
File Location       : samples/estat_tran_hv_frmod.csv (cleaned: samples/eurostat_*_clean.csv)
Data Format         : CSV (converted from TSV)
Key Variables       : freq, unit, tra_mode (IWW/RAIL/ROAD/RAIL_IWW_AVD), geo, yearly percentages
Data Quality        : ⭐⭐⭐⭐⭐ (5/5) - Official Eurostat data, 86.5% complete, standardized methodology
Limitations         : 13.5% missing values (some countries lack IWW data), estimated values marked with flags
Update Frequency    : Annual
Contact Info        : Eurostat User Support: estat-user-support@ec.europa.eu
Notes               : Modal split = % distribution of freight across transport modes.
                      Belgium shows 10-11% IWW usage (strong).
                      Overall EU trend declining -5.6% from 2005-2023.
```

---

## 📚 Command Reference

### TSV to CSV Conversion

```bash
# Basic conversion
python scripts/tsv_to_csv.py input.tsv

# Specify output
python scripts/tsv_to_csv.py input.tsv -o output.csv

# Convert and analyze
python scripts/tsv_to_csv.py input.tsv --process

# Batch convert directory
python scripts/tsv_to_csv.py --dir ./data
```

### Data Cleaning

```bash
# Basic cleaning with stats
python scripts/clean_eurostat.py data.csv --stats

# Filter by geography
python scripts/clean_eurostat.py data.csv --geo BE NL DE

# Filter by transport mode
python scripts/clean_eurostat.py data.csv --mode IWW RAIL

# Combine filters
python scripts/clean_eurostat.py data.csv --geo BE --mode IWW --stats --trends

# Export cleaned data
python scripts/clean_eurostat.py data.csv --geo BE --output cleaned.csv

# Long format
python scripts/clean_eurostat.py data.csv --long --output long.csv
```

### Inventory Management

```bash
# Create template
python scripts/simple_inventory.py template inventory_template.csv

# Add entry (interactive)
python scripts/simple_inventory.py add --interactive

# Add entry (command-line)
python scripts/simple_inventory.py add \
  --source-id ID_001 \
  --topic Transport \
  --name "Source Name" \
  --url "https://..." \
  --file "path/to/file.csv"

# List all entries
python scripts/simple_inventory.py list

# List by topic
python scripts/simple_inventory.py list --topic Transport

# Show specific entry
python scripts/simple_inventory.py show ESTAT_HV_001

# Search inventory
python scripts/simple_inventory.py search "keyword"

# Delete entry
python scripts/simple_inventory.py delete ID_001
```

---

## 💡 Tips & Best Practices

### Source ID Naming Convention

Use a consistent pattern:
- `ESTAT_XXX` - Eurostat data
- `STATBEL_XXX` - StatBel (Belgian statistics)
- `ITB_XXX` - ITB internal data
- `PORT_XXX` - Port authority data
- `VIA_XXX` - VIA (Flemish Waterway Authority)

### Topic Categories

Suggested topics:
- **Transport** - Modal split, freight, passenger
- **Economics** - Trade, GDP, prices
- **Fleet Management** - Vessel data, registrations
- **Operations** - Traffic, cargo handling
- **Environment** - Emissions, water quality
- **Infrastructure** - Ports, waterways, locks
- **Labor Market** - Employment, skills
- **Safety** - Incidents, regulations

### Data Quality Rating

Use this guide:
- ⭐ (1/5) - Poor quality, major issues
- ⭐⭐ (2/5) - Limited quality, significant gaps
- ⭐⭐⭐ (3/5) - Good quality, minor limitations
- ⭐⭐⭐⭐ (4/5) - Very good quality, reliable
- ⭐⭐⭐⭐⭐ (5/5) - Excellent quality, official/authoritative

### File Organization

Recommended structure:
```
data-inventory/
├── samples/           # Original data files
├── cleaned/           # Cleaned/filtered data
├── analysis/          # Analysis outputs
├── data_inventory_simple.csv  # Main inventory
└── scripts/           # Processing scripts
```

---

## 🎯 Next Steps

1. **Process more data sources** - Add ITB fleet data, port statistics, etc.
2. **Automate workflows** - Create bash scripts for common tasks
3. **Visualize data** - Add plotting capabilities
4. **Share inventory** - Export to Excel for team sharing
5. **Integrate systems** - Link inventory with analysis tools

---

## 📞 Support

For questions about:
- **Eurostat data**: estat-user-support@ec.europa.eu
- **This workflow**: See repository documentation
- **Data sources**: Contact info in inventory

---

*Last updated: 2025-10-23*
