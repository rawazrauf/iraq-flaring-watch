# Data Methodology — Iraq Flaring Watch

This document explains how each dataset used in Iraq Flaring Watch was sourced, processed, and integrated into the map.

---

## 1. Active Flare Locations (`query`)

**Source:** OpenStreetMap via Overpass API  
**Tag:** `man_made=flare`  
**Coverage:** All of Iraq  

### How it was generated

The preloaded dataset is a snapshot queried from the OpenStreetMap Overpass API using:

```
[out:json][timeout:60];
area["ISO3166-1"="IQ"]->.searchArea;
(
  node["man_made"="flare"](area.searchArea);
  way["man_made"="flare"](area.searchArea);
);
out center;
```

The result is stored as `query` in the repo root. The map also supports live querying against three Overpass endpoints with automatic failover.

Field detection (assigning flares to named oil fields) uses a proximity lookup against 24 known field centroids within a 0.25° radius threshold.

---

## 2. Population Exposure (`query_population.json`)

**Source:** WorldPop Project — Iraq 2020 UN-adjusted constrained population raster  
**File:** `irq_ppp_2020_UNadj_constrained.tif`  
**Resolution:** ~100m per pixel  
**Projection:** EPSG:4326 (WGS84), reprojected to EPSG:32638 (UTM Zone 38N) for accurate buffering  

### How it was generated

Run locally in Google Colab or any Python environment with the raster file present:

```python
!pip install rasterio pyproj shapely requests

import json, rasterio, numpy as np, pyproj, requests
from rasterio.mask import mask
from shapely.geometry import Point
from shapely.ops import transform

# Fetch current flare coordinates from GitHub
url = "https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/query"
flare_data = requests.get(url).json()

# Setup UTM Zone 38N projection for accurate 5km buffering
project_to_meters = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32638", always_xy=True).transform
project_to_degrees = pyproj.Transformer.from_crs("EPSG:32638", "EPSG:4326", always_xy=True).transform

population_dict = {}

with rasterio.open('irq_ppp_2020_UNadj_constrained.tif') as src:
    for el in flare_data['elements']:
        lat = el.get('lat') or el.get('center', {}).get('lat')
        lon = el.get('lon') or el.get('center', {}).get('lon')
        if not lat or not lon: continue

        # Buffer 5000m in UTM, reproject back to degrees for raster masking
        point_meters = transform(project_to_meters, Point(lon, lat))
        circle_meters = point_meters.buffer(5000)
        circle_degrees = transform(project_to_degrees, circle_meters)

        try:
            out_image, _ = mask(src, [circle_degrees], crop=True)
            pop_sum = int(np.nansum(out_image[out_image > 0]))
            population_dict[str(el['id'])] = pop_sum
        except ValueError:
            population_dict[str(el['id'])] = 0  # Flare outside raster bounds

with open('query_population.json', 'w') as f:
    json.dump(population_dict, f, indent=4)
```

The script fetches the latest `query` file from GitHub automatically, so re-running it after adding new flares to OSM will generate a fully updated `query_population.json`.

**Output:** A flat JSON dictionary mapping OSM element IDs to integer population counts within 5km.

---

## 3. Emission Plumes (`iraq_tanager_plumes.json`)

**Source:** Carbon Mapper — Tanager satellite  
**Coverage:** Iraq, 2024–2025  
**Gas types:** CH₄ (methane) and CO₂  

### Fields per record

| Field | Description |
|---|---|
| `lat`, `lon` | Plume centroid coordinates |
| `gas` | Gas type: `CH4` or `CO2` |
| `emission_kghr` | Emission rate in kg/hr |
| `sector` | IPCC sector code (e.g. `1B2` = Oil & Gas Fugitive) |
| `wind_speed_ms` | Wind speed at detection time (m/s) |
| `timestamp` | Detection datetime (ISO 8601) |
| `plume_png` | URL to satellite detection image |
| `plume_bounds` | Bounding box `[west, south, east, north]` |
| `portal_url` | Link to Carbon Mapper portal entry |

### Visualisation

Circle radius is scaled logarithmically by emission rate: `Math.max(6, Math.min(22, Math.log10(emission) * 4))`. All plumes are rendered in cyan (`#06b6d4`) with white border regardless of gas type — the popup card shows the gas type detail.

---

## 4. Gas Volume & Economic Waste (`iraq_wb_flares_all_years.json`)

**Source:** World Bank Global Gas Flaring Reduction Partnership (GGFR)  
**Dataset:** 2012–2024 Flare Volume Estimates by Individual Flare Location  
**URL:** https://www.worldbank.org/en/programs/gasflaringreduction/global-flaring-data  

### How it was generated

Filtered from the World Bank Excel file to Iraq only, all years, then restructured as a year-keyed JSON:

```python
import pandas as pd, json

df = pd.read_excel('2012-2024-Flare-Volume-Estimates-by-individual-Flare-Location.xlsx')
iraq = df[df['Country'] == 'Iraq'].copy()

output = {}
for year in sorted(iraq['Year'].unique()):
    yr_df = iraq[iraq['Year'] == year]
    records = []
    for _, row in yr_df.iterrows():
        records.append({
            'lat':      round(float(row['Latitude']), 6),
            'lon':      round(float(row['Longitude']), 6),
            'year':     int(row['Year']),
            'field':    str(row['Field Name'])      if pd.notna(row['Field Name'])      else None,
            'type':     str(row['Field  Type'])     if pd.notna(row['Field  Type'])     else None,
            'operator': str(row['Field  Operator']) if pd.notna(row['Field  Operator']) else None,
            'location': str(row['Location'])        if pd.notna(row['Location'])        else None,
            'level':    str(row['Flare Level'])     if pd.notna(row['Flare Level'])     else None,
            'vol_mm3':  round(float(row['Flaring Vol (million m3)']), 6),
            'bcm':      round(float(row['bcm']), 8),
            'mmscfd':   round(float(row['MMscfd']), 6)
        })
    output[str(int(year))] = records

with open('iraq_wb_flares_all_years.json', 'w') as f:
    json.dump(output, f)
```

**Total records:** 2,404 (Iraq only, 2012–2024, including zero-volume entries)

### Economic value calculation

```
GAS_PRICE_MMBTU = 3.50   # USD per MMBtu (conservative global benchmark)

valueUSD_millions = vol_mm3 × 35,315 × GAS_PRICE_MMBTU / 1,000,000
```

**Unit explanation:**
- `vol_mm3` is in millions of cubic metres per year
- 1 million m³ = 35,315 MMBtu
- Dividing by 1,000,000 converts USD to USD millions

### Electricity equivalent calculation

```
homesEquivalent = (vol_mm3 × 4,400 × 1,000) / 4,500
```

**Assumptions:**
- Gas-to-electricity conversion: ~4,400 kWh per thousand m³ at 35% plant efficiency
- Iraqi household annual consumption: 4,500 kWh/year

### Display filter

Sites with estimated value loss below $1M/year are excluded from the map to reduce clutter. This threshold corresponds to approximately 8,100 M m³/year equivalent.

### Bubble sizing

```
radius = Math.max(6, Math.min(45, Math.pow(vol_mm3, 0.4) × 1.5))
```

Power scaling (`^0.4`) provides readable differentiation across the full range from ~2 M m³ to 1,642 M m³.

---

## Key national figures (Iraq, 2024)

| Metric | Value |
|---|---|
| National flaring total | ~18,182 M m³/yr |
| Largest single site | West Qurna 2 (LUKOIL), 1,642 M m³/yr |
| Estimated value — West Qurna 2 | ~$202M/yr |
| Iraqi homes — West Qurna 2 equivalent | ~1.6 million |
| Total WB records displayed (≥$1M) | ~170 sites |
