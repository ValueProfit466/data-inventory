#!/usr/bin/env python3
"""
Populate inventory with complete Eurostat entry
"""
from simple_inventory import SimpleInventory
from pathlib import Path
from datetime import date

# Initialize inventory
inventory = SimpleInventory(Path('data_inventory_simple.csv'))
inventory.load()

# Complete Eurostat entry
eurostat_entry = {
    'Source ID': 'ESTAT_HV_001',
    'Topic': 'Transport',
    'Source Name': 'Eurostat Heavy Vehicle Freight Modal Split',
    'URL': 'https://ec.europa.eu/eurostat/databrowser/view/tran_hv_frmod/',
    'Date Accessed': str(date.today()),
    'Data Years': '2005-2023 (annual)',
    'Geographic Scope': 'EU27, EU28, 32 European countries',
    'File Location': 'samples/estat_tran_hv_frmod.csv (cleaned: samples/eurostat_*_clean.csv)',
    'Data Format': 'CSV (converted from TSV)',
    'Key Variables': 'freq, unit, tra_mode (IWW/RAIL/ROAD/RAIL_IWW_AVD), geo, yearly percentages',
    'Data Quality': '⭐⭐⭐⭐⭐ (5/5) - Official Eurostat data, 86.5% complete, standardized methodology',
    'Limitations': '13.5% missing values (some countries lack IWW data), estimated values marked with flags, no sub-annual frequency',
    'Update Frequency': 'Annual',
    'Contact Info': 'Eurostat User Support: estat-user-support@ec.europa.eu',
    'Notes': 'Modal split = % distribution of freight across transport modes. Cleaned using clean_eurostat.py. Belgium shows 10-11% IWW usage (strong). Overall EU trend declining -5.6% from 2005-2023.'
}

# Delete existing entry if present (avoid interactive prompt)
if 'ESTAT_HV_001' in inventory.df['Source ID'].values:
    inventory.df = inventory.df[inventory.df['Source ID'] != 'ESTAT_HV_001']

# Add entry
inventory.add_entry(eurostat_entry)
inventory.save()

print("\n✓ Inventory updated with complete Eurostat entry")
