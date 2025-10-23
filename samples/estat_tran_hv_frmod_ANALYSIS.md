# Eurostat Transport Data Analysis
## File: estat_tran_hv_frmod.tsv

**Generated:** October 23, 2025
**Dataset Source:** Eurostat (European Statistics)

---

## Dataset Overview

This is a **Eurostat Heavy Vehicles Freight Modal Split** dataset containing transport statistics across European countries from 2005 to 2023.

### Key Facts
- **128 rows** of transport data
- **32 countries/regions** covered
- **19 years** of time-series data (2005-2023)
- **4 transport modes** tracked
- **86.5% data completeness** (13.5% missing values)

---

## Dataset Structure

### Metadata Fields (Column 1)
The first column contains comma-separated metadata:
- **freq**: Frequency (A = Annual)
- **unit**: Unit of measurement (PC = Percentage)
- **tra_mode**: Transport mode
- **geo**: Geographic region (country code)

Example: `A,PC,IWW,BE` = Annual, Percentage, Inland Waterway, Belgium

### Time Period Columns (Columns 2-20)
Years from 2005 to 2023, each containing percentage values.

---

## Transport Modes Analyzed

1. **IWW** - Inland Waterway (32 rows)
2. **RAIL** - Rail Transport (32 rows)
3. **RAIL_IWW_AVD** - Rail + Inland Waterway Average (32 rows)
4. **ROAD** - Road Transport (32 rows)

Each mode has data for 32 geographic regions.

---

## Geographic Coverage

**32 Countries/Regions:**

EU Aggregates:
- EU27_2020 (27 member states as of 2020)
- EU28 (28 member states, includes UK)

Individual Countries:
AT (Austria), BE (Belgium), BG (Bulgaria), CH (Switzerland), CY (Cyprus),
CZ (Czechia), DE (Germany), DK (Denmark), EE (Estonia), EL (Greece),
ES (Spain), FI (Finland), FR (France), HR (Croatia), HU (Hungary),
IE (Ireland), IT (Italy), LT (Lithuania), LU (Luxembourg), LV (Latvia),
MT (Malta), NL (Netherlands), NO (Norway), PL (Poland), PT (Portugal),
RO (Romania), SE (Sweden), SI (Slovenia), SK (Slovakia), UK (United Kingdom)

---

## Data Quality Assessment

### Completeness
- **Valid values:** 2,104 cells (86.5%)
- **Missing/Not available:** 328 cells (13.5%)
- **Estimated values (e):** 258 cells (10.6%)
- **Break in series (b):** 0 cells (0.0%)

### Data Flags Explained
- **e** = Estimated value
- **b** = Break in time series
- **n** = Not significant
- **:** = Not available
- **m** = Missing

### Countries with Missing Data
Some countries have no inland waterway data (landlocked or no navigable waterways):
- Cyprus (CY) - Island nation
- Denmark (DK) - Minimal inland waterways
- Estonia (EE), Greece (EL) - Limited data

---

## Key Statistical Findings

### Overall Trend (2005-2023)
- **2005 Average:** 36.98%
- **2023 Average:** 34.92%
- **Change:** -2.06 percentage points (-5.6%)

This indicates a slight **decline in the modal share** over the 19-year period.

### Year-by-Year Statistics

| Year | Data Points | Mean  | Median | Min  | Max    |
|------|-------------|-------|--------|------|--------|
| 2005 | 112         | 36.98 | 29.05  | 0.00 | 100.00 |
| 2010 | 112         | 36.95 | 29.55  | 0.00 | 100.00 |
| 2015 | 112         | 36.44 | 27.75  | 0.00 | 100.00 |
| 2020 | 105         | 35.89 | 28.80  | 0.00 | 100.00 |
| 2023 | 105         | 34.92 | 24.20  | 0.00 | 100.00 |

### Notable Observations
1. **Consistent decline:** Mean values decrease steadily from 36.98% (2005) to 34.92% (2023)
2. **Median decline:** Median drops more significantly from 29.05% to 24.20%
3. **Data availability:** 112 data points for earlier years, 105 for recent years
4. **Full range:** Values span from 0% to 100%, indicating diverse modal splits

---

## Sample Country Data (Recent Years)

### Inland Waterway Modal Share (2021-2023)

| Country | 2021   | 2022   | 2023   | Trend |
|---------|--------|--------|--------|-------|
| AT      | 2.1%   | 1.7%   | 1.7%   | ↓     |
| BE      | 11.5%  | 11.2%  | 10.7%  | ↓     |
| BG      | 24.4%  | 16.6%  | 17.9%  | ↓↑    |
| CH      | 0.1%   | 0.1%   | 0.1%   | →     |
| DE      | 7.4%   | 6.8%   | 6.6%   | ↓     |

**Insights:**
- **Belgium** maintains relatively high inland waterway usage (10-11%)
- **Bulgaria** shows high but volatile percentages
- **Switzerland** has minimal inland waterway transport
- **Germany** shows steady decline in recent years

---

## Use Cases for This Data

### 1. Transportation Planning
- Evaluate modal shift policies
- Identify countries with strong inland waterway infrastructure
- Track progress toward sustainable transport goals

### 2. Infrastructure Investment
- Identify regions where waterway transport is viable
- Compare road vs. rail vs. waterway usage patterns
- Assess market opportunities for inland port development

### 3. Environmental Analysis
- Modal shift from road to waterway reduces emissions
- Track progress toward EU Green Deal transport goals
- Analyze sustainability trends in freight transport

### 4. Economic Research
- Correlate transport modes with economic development
- Study impact of EU policies on transport choices
- Analyze competitiveness of different transport modes

---

## Data Access

### Files Generated
1. **estat_tran_hv_frmod.tsv** - Original Eurostat TSV file
2. **estat_tran_hv_frmod.csv** - Converted CSV file (easier to process)

### How to Work With This Data

#### Quick Analysis
```bash
# Convert and analyze
python scripts/tsv_to_csv.py samples/estat_tran_hv_frmod.tsv --process

# Detailed analysis
python scripts/analyze_eurostat.py
```

#### Python Processing
```python
import pandas as pd

# Read the CSV
df = pd.read_csv('samples/estat_tran_hv_frmod.csv')

# Filter for specific country (e.g., Belgium)
belgium_data = df[df['freq,unit,tra_mode,geo\\TIME_PERIOD'].str.contains('BE')]

# Filter for specific transport mode (e.g., inland waterway)
iww_data = df[df['freq,unit,tra_mode,geo\\TIME_PERIOD'].str.contains('IWW')]

# Extract time series for a specific country and mode
be_iww = df[df['freq,unit,tra_mode,geo\\TIME_PERIOD'] == 'A,PC,IWW,BE']
```

---

## Dataset Context

### What is Modal Split?
Modal split (or modal share) refers to the **percentage distribution of freight transport** across different modes:
- **Road** (trucks, lorries)
- **Rail** (freight trains)
- **Inland Waterway** (barges, river transport)
- **Pipeline** (not in this dataset)
- **Air** (not in this dataset)

### Why It Matters
- **Environmental Impact:** Waterway and rail transport produce fewer emissions per ton-km than road
- **Congestion:** Shifting freight from roads reduces traffic congestion
- **Cost Efficiency:** Water and rail can be more economical for bulk goods
- **EU Policy:** EU promotes modal shift away from road transport

---

## Integration with Data Inventory

This Eurostat dataset can be integrated into your ITB data inventory system:

1. **Add to inventory** using `fill_inventory.py`:
   - Source: Eurostat
   - Domain: economisch / operationeel
   - Geographic coverage: EU27_2020, multiple countries
   - Update frequency: annual
   - Data status: Volledig

2. **Quality assessment**:
   - Completeness: 3 (86.5% complete)
   - Accuracy: 3 (official Eurostat data)
   - Timeliness: 3 (up to 2023)
   - Accessibility: 3 (publicly available)

---

## Next Steps

### Recommended Actions
1. ✅ **Converted** TSV to CSV format
2. ✅ **Analyzed** data structure and quality
3. ⬜ **Filter** data for specific countries of interest (e.g., Belgium, Netherlands)
4. ⬜ **Visualize** trends over time
5. ⬜ **Compare** with ITB's own fleet and traffic data
6. ⬜ **Integrate** into master data inventory

### Advanced Analysis Opportunities
- Time-series forecasting for modal split trends
- Country comparison dashboards
- Correlation with economic indicators
- Impact assessment of EU transport policies

---

## References

- **Source:** Eurostat (European Commission)
- **Dataset Code:** estat_tran_hv_frmod
- **Unit:** Percentage (PC)
- **Frequency:** Annual (A)
- **Last Update:** 2023 data
- **URL:** https://ec.europa.eu/eurostat/

---

*Analysis generated using tsv_to_csv.py and analyze_eurostat.py*
