# ITB Data Inventory

**Streamlined data source management for ITB (Inland Transport Belgium/Vlaanderen)**

Manage, process, and catalog external data sources with automated cleaning, filtering, and quality assessment.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Convert TSV data to CSV
python scripts/tsv_to_csv.py data.tsv --process

# 3. Clean and filter data
python scripts/clean_eurostat.py data.csv --geo BE NL --stats --output cleaned.csv

# 4. Add to inventory
python scripts/simple_inventory.py add --interactive
```

---

## 📚 Documentation

- **[WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)** - Complete end-to-end workflow
- **[TSV_TO_CSV_GUIDE.md](TSV_TO_CSV_GUIDE.md)** - TSV/CSV conversion guide

---

## 🛠 Tools

### 1. **tsv_to_csv.py** - Format Conversion
Convert TSV files to CSV and analyze structure
```bash
python scripts/tsv_to_csv.py input.tsv --process
```

### 2. **clean_eurostat.py** - Data Cleaning
Clean Eurostat data, filter by geography and variables
```bash
python scripts/clean_eurostat.py data.csv --geo BE NL --mode IWW --stats --output cleaned.csv
```

### 3. **simple_inventory.py** - Inventory Management
Simplified data source catalog with 15 key fields
```bash
python scripts/simple_inventory.py add --interactive
python scripts/simple_inventory.py list
python scripts/simple_inventory.py show ESTAT_HV_001
```

---

## 📊 Simplified Inventory Schema

The new streamlined inventory tracks:

- **Source ID** - Unique identifier
- **Topic** - Subject area (Transport, Economics, etc.)
- **Source Name** - Data source name
- **URL** - Web address or access method
- **Date Accessed** - When data was obtained
- **Data Years** - Time period covered
- **Geographic Scope** - Geographic coverage
- **File Location** - Path to local files
- **Data Format** - CSV, Excel, JSON, etc.
- **Key Variables** - Main variables/columns
- **Data Quality** - Quality rating (1-5 stars) and notes
- **Limitations** - Known issues
- **Update Frequency** - How often source updates
- **Contact Info** - Contact person/organization
- **Notes** - Additional information

---

## 📁 Repository Structure

```
data-inventory/
├── README.md                    # This file
├── WORKFLOW_GUIDE.md            # Complete workflow documentation
├── TSV_TO_CSV_GUIDE.md         # Conversion guide
├── requirements.txt             # Python dependencies
├── data_inventory_simple.csv    # Main inventory file
├── config/
│   └── inventory_config.yaml    # Configuration (legacy)
├── samples/
│   ├── estat_tran_hv_frmod.tsv # Example: Eurostat transport data
│   ├── estat_tran_hv_frmod.csv # Converted to CSV
│   ├── eurostat_*_clean.csv    # Cleaned/filtered versions
│   └── example_data.tsv        # Simple example
└── scripts/
    ├── tsv_to_csv.py           # TSV to CSV converter
    ├── clean_eurostat.py       # Eurostat data cleaner
    ├── simple_inventory.py     # Inventory manager
    ├── analyze_eurostat.py     # Detailed Eurostat analysis
    ├── populate_inventory.py   # Example: populate inventory
    └── fill_inventory.py       # Legacy inventory tool
```

---

## 🎯 Example Workflow: Eurostat Data

```bash
# 1. Convert TSV to CSV
python scripts/tsv_to_csv.py samples/estat_tran_hv_frmod.tsv

# 2. Clean and filter for Belgium
python scripts/clean_eurostat.py samples/estat_tran_hv_frmod.csv \
  --geo BE \
  --stats \
  --trends \
  --output samples/eurostat_belgium_clean.csv

# 3. Add to inventory
python scripts/simple_inventory.py add \
  --source-id ESTAT_HV_001 \
  --topic Transport \
  --name "Eurostat Heavy Vehicle Freight Modal Split" \
  --url "https://ec.europa.eu/eurostat/databrowser/view/tran_hv_frmod/" \
  --file "samples/estat_tran_hv_frmod.csv" \
  --format CSV \
  --years "2005-2023" \
  --geo "EU27, 32 countries"

# 4. View entry
python scripts/simple_inventory.py show ESTAT_HV_001
```

---

## 📖 Features

### Data Processing
- ✅ TSV to CSV conversion
- ✅ Eurostat flag removal (e, p, b, n, etc.)
- ✅ Geographic filtering
- ✅ Variable/dimension filtering
- ✅ Wide to long format reshaping
- ✅ Summary statistics
- ✅ Trend analysis

### Inventory Management
- ✅ Simplified 15-field schema
- ✅ Interactive and command-line modes
- ✅ Search and filter capabilities
- ✅ CSV and Excel export
- ✅ Template generation
- ✅ Quality rating system (1-5 stars)

### Analysis
- ✅ Data quality assessment
- ✅ Completeness statistics
- ✅ Time-series analysis
- ✅ Country comparisons
- ✅ Modal split analysis

---

## 💡 Use Cases

1. **Transport Planning** - Track modal split trends for policy decisions
2. **Data Discovery** - Know what data sources you have
3. **Quality Assessment** - Evaluate data completeness and reliability
4. **Compliance** - Document data sources for reporting
5. **Research** - Find relevant datasets quickly
6. **Integration** - Prepare data for analysis platforms

---

## 🔧 Requirements

```
pandas>=2.0.0
pyyaml>=6.0
openpyxl>=3.0.0
xlsxwriter>=3.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 📊 Example: Eurostat Transport Data

The repository includes a complete example using Eurostat's Heavy Vehicle Freight Modal Split data:

- **128 rows** of transport statistics
- **32 European countries**
- **19 years** (2005-2023)
- **4 transport modes** (Road, Rail, Inland Waterway, Combined)
- **86.5% data completeness**

Key findings:
- Netherlands: 43.5% inland waterway modal share (highest in EU)
- Belgium: 13.5% inland waterway (strong performer)
- Overall EU trend: -5.6% decline from 2005-2023

---

## 🎓 Getting Started

1. **Read the guides**
   - Start with [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
   - Check [TSV_TO_CSV_GUIDE.md](TSV_TO_CSV_GUIDE.md) for conversions

2. **Try the example**
   ```bash
   python scripts/tsv_to_csv.py samples/estat_tran_hv_frmod.tsv --process
   python scripts/clean_eurostat.py samples/estat_tran_hv_frmod.csv --geo BE --stats
   ```

3. **Create your inventory**
   ```bash
   python scripts/simple_inventory.py template my_inventory.csv
   python scripts/simple_inventory.py --inventory my_inventory.csv add --interactive
   ```

4. **Process your data**
   - Add your TSV/CSV files to `samples/`
   - Run conversion and cleaning scripts
   - Add entries to inventory

---

## 📞 Support

For questions about specific data sources, see the **Contact Info** field in the inventory.

For issues with this repository, please check the documentation or create an issue.

---

## 📝 License

[Add your license information here]

---

**ITB Data Inventory** - Simplifying data management for inland waterway transport research and operations.
