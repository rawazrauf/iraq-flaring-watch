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
**API:** https://api.carbonmapper.org/api/v1/catalog/plumes/annotated  
**Coverage:** Iraq, all available Tanager detections  
**Gas types:** CH₄ (methane) and CO₂  

### How it was generated

Requires a Carbon Mapper API token. Run in Python:

```python
import requests, json, time
from collections import Counter

headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Accept": "application/json"
}

# Iraq bounding box
IRAQ = {"lon_min": 38.797, "lon_max": 48.569, "lat_min": 29.059, "lat_max": 37.378}

def in_iraq(lon, lat):
    return (IRAQ["lon_min"] <= lon <= IRAQ["lon_max"] and
            IRAQ["lat_min"] <= lat <= IRAQ["lat_max"])

all_iraq_plumes = []
LIMIT = 500

for gas in ["CH4", "CO2"]:
    offset = 0
    pages_checked = 0

    # Get total count first
    r = requests.get(
        "https://api.carbonmapper.org/api/v1/catalog/plumes/annotated",
        headers=headers,
        params={"instrument": "tan", "gas": gas, "limit": 1, "offset": 0}
    )
    total = r.json().get("total_count", 0)
    print(f"\n{gas}: {total} total Tanager plumes globally, scanning for Iraq...")

    while offset < total:
        r = requests.get(
            "https://api.carbonmapper.org/api/v1/catalog/plumes/annotated",
            headers=headers,
            params={"instrument": "tan", "gas": gas, "limit": LIMIT, "offset": offset, "sort": "desc"}
        )
        items = r.json().get("items", [])
        if not items:
            break

        iraq_batch = [
            {
                "plume_id":                    p["plume_id"],
                "gas":                         p["gas"],
                "lat":                         p["geometry_json"]["coordinates"][1],
                "lon":                         p["geometry_json"]["coordinates"][0],
                "timestamp":                   p["scene_timestamp"],
                "emission_kghr":               p.get("emission_auto"),
                "emission_uncertainty_kghr":   p.get("emission_uncertainty_auto"),
                "sector":                      p.get("sector"),
                "wind_speed_ms":               p.get("wind_speed_avg_auto"),
                "wind_direction_deg":          p.get("wind_direction_avg_auto"),
                "plume_png":                   p.get("plume_png", "").split("?")[0].replace(
                                                   "https://catalog.carbonmapper.org/",
                                                   "https://api.carbonmapper.org/api/v1/catalog/asset/"
                                               ) if p.get("plume_png") else None,
                "plume_bounds":                p.get("plume_bounds"),
                "plume_quality":               p.get("plume_quality"),
                "instrument":                  p.get("instrument"),
                "platform":                    p.get("platform"),
                "portal_url":                  f"https://data.carbonmapper.org/?instruments=tan&details={p.get('gas', '')}_{p.get('sector', 'other')}_250m_{p['geometry_json']['coordinates'][0]:.5f}_{p['geometry_json']['coordinates'][1]:.5f}%3Finstruments%3Dtan%26status%3Dnot_deleted&plume_id={p['plume_id']}#13/{p['geometry_json']['coordinates'][1]:.4f}/{p['geometry_json']['coordinates'][0]:.4f}"
            }
            for p in items
            if in_iraq(p["geometry_json"]["coordinates"][0], p["geometry_json"]["coordinates"][1])
        ]

        all_iraq_plumes.extend(iraq_batch)
        pages_checked += 1
        offset += LIMIT

        if pages_checked % 10 == 0:
            iraq_count = len([p for p in all_iraq_plumes if p['gas'] == gas])
            print(f"  {gas} | scanned {offset}/{total} | Iraq found so far: {iraq_count}")

        time.sleep(0.15)

# Summary
ch4 = [p for p in all_iraq_plumes if p["gas"] == "CH4"]
co2 = [p for p in all_iraq_plumes if p["gas"] == "CO2"]
print(f"\n=== IRAQ TANAGER RESULTS ===")
print(f"CH4 plumes: {len(ch4)}")
print(f"CO2 plumes: {len(co2)}")
print(f"Total: {len(all_iraq_plumes)}")

emissions = [p["emission_kghr"] for p in all_iraq_plumes if p.get("emission_kghr")]
if emissions:
    print(f"\nEmission rates (kg/hr):")
    print(f"  Count: {len(emissions)}")
    print(f"  Min:   {min(emissions):.1f}")
    print(f"  Max:   {max(emissions):.1f}")
    print(f"  Avg:   {sum(emissions)/len(emissions):.1f}")

with open("iraq_tanager_plumes.json", "w") as f:
    json.dump(all_iraq_plumes, f, indent=2)
print(f"\nSaved to iraq_tanager_plumes.json")
```

The script paginates through the full global Tanager catalogue in batches of 500, filtering to Iraq's bounding box (38.797°E–48.569°E, 29.059°N–37.378°N). A 0.15s delay between requests respects the API rate limit. Both CH4 and CO2 are fetched in separate passes.

### Fields per record

| Field | Description |
|---|---|
| `lat`, `lon` | Plume centroid coordinates |
| `gas` | Gas type: `CH4` or `CO2` |
| `emission_kghr` | Emission rate in kg/hr (auto-quantified) |
| `emission_uncertainty_kghr` | Uncertainty range in kg/hr |
| `sector` | IPCC sector code (e.g. `1B2` = Oil & Gas Fugitive) |
| `wind_speed_ms` | Wind speed at detection time (m/s) |
| `wind_direction_deg` | Wind direction at detection time (degrees) |
| `timestamp` | Detection datetime (ISO 8601) |
| `plume_png` | URL to satellite detection image |
| `plume_bounds` | Bounding box `[west, south, east, north]` |
| `plume_quality` | Carbon Mapper quality flag |
| `instrument` | Always `tan` (Tanager) |
| `platform` | Satellite platform identifier |
| `portal_url` | Link to Carbon Mapper data portal entry |

### Visualisation

Circle radius is scaled logarithmically by emission rate: `Math.max(6, Math.min(22, Math.log10(emission) * 4))`. All plumes are rendered in cyan (`#06b6d4`) with white border regardless of gas type — the popup card shows the gas type and full metadata.

---

## 4. Gas Volume & Economic Waste (`iraq_wb_flares_all_years.json`)

**Source:** World Bank Global Gas Flaring Reduction Partnership (GGFR)  
**Dataset:** 2012–2025 Flare Volume Estimates by Individual Flare Location  
**URL:** https://www.worldbank.org/en/programs/gasflaringreduction/global-flaring-data  

### How it was generated

Filtered from the World Bank Excel file to Iraq only, all years, then restructured as a year-keyed JSON. The map displays the most recent year (**2025**); earlier years are retained in the file for historical comparison.

```python
import pandas as pd, json

df = pd.read_excel('Flare-Volume-Estimates-by-individual-Flare-Location-2012-2025.xlsx')
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

**Total records:** 4,144 across all years (Iraq only, 2012–2025, including zero-volume entries). The displayed 2025 year holds 296 records.

### Economic value calculation

```
GAS_PRICE_MMBTU = 3.50   # USD per MMBtu

valueUSD_millions = vol_mm3 × 35,315 × GAS_PRICE_MMBTU / 1,000,000
```

**Unit explanation:**
- `vol_mm3` is in millions of cubic metres per year
- 1 million m³ = 35,315 MMBtu
- Dividing by 1,000,000 converts USD to USD millions

**Price basis:**
$3.50/MMBtu is the minimum domestic gas price officially adopted by the Iraqi Council of Ministers in Cabinet Session 49 (2025), as published by the Prime Minister's Office:
https://pmo.iq/?article=3907

This rate is also consistent with the World Bank GGFR methodology for associated gas valuation in producing countries without LNG export infrastructure. S&P Global Commodity Insights (July 2025) separately estimates Iraq's flared gas capture cost at ~$2/MMBtu against import prices of ~$8/MMBtu, placing the $3.50/MMBtu figure within a well-supported range.

### Electricity equivalent calculation

```
mwPotential     = (vol_mm3 × 4,400 × 0.35) / 8,760
homesEquivalent = (vol_mm3 × 4,400 × 1,000) / 5,000
```

**Assumptions:**
- Gas-to-electricity conversion: ~4,400 kWh per thousand m³ at 35% plant efficiency
- Continuous generation basis: 8,760 hours/year (for the MW capacity figure)
- Iraqi household annual consumption: 5,000 kWh/year
- Derived from IEA Iraq electricity data (1.377 MWh/capita) × 2024 census 
  (46.12M population ÷ 8.05M households = 5.73 persons/household), 
  assuming 60-65% residential share of total consumption
- Methodology reviewed by Ahmed Gailani, Senior Energy Modeller at NESO 
  (National Energy System Operator, Great Britain)
  https://scholar.google.com/citations?user=IpmavsIAAAAJ&hl=en

### Display filter

Sites with estimated value loss below $1M/year are excluded from the map to reduce clutter. This threshold corresponds to approximately 8.1 M m³/year equivalent (1,000,000 ÷ 35,315 ÷ 3.50).

### Bubble sizing

```
radius = Math.max(6, Math.min(45, Math.pow(vol_mm3, 0.4) × 1.5))
```

Power scaling (`^0.4`) provides readable differentiation across the full range from ~2 M m³ to ~2,755 M m³.

---

## Key national figures (Iraq, 2025)

Computed from the displayed 2025 World Bank slice using the formulas above.

| Metric | Value |
|---|---|
| National flaring total | ~24,122 M m³/yr (~24.1 BCM) |
| Estimated value of wasted gas | ~$2.98 billion/yr |
| Electricity generation potential | ~4,241 MW |
| People within 5 km of a flare | ~5.2 million |
| Largest single site | West Qurna 2 – Yamama (LUKOIL), ~2,755 M m³/yr |
| Estimated value — West Qurna 2 | ~$341M/yr |
| Total WB records displayed (≥$1M) | ~136 sites |
---

## 5. Population Impact (`iraq_flaring_impact.json`)

**Source:** WorldPop Project — Iraq 2020 UN-adjusted constrained population raster  
**Script:** `population_impact.py` (repo root)  
**Output:** `iraq_flaring_impact.json` (repo root)  

### How it was generated

Run `population_impact.py` in Google Colab with `irq_ppp_2020_UNadj_constrained.tif` uploaded to the session. The script fetches the latest flare locations from GitHub automatically, so re-running after adding new flares to OSM will produce an updated figure.

### Methodology

Each flare is buffered by 5km in UTM Zone 38N (EPSG:32638) for accurate metric distance calculation. All 5km circles are unioned into a single polygon using `shapely.ops.unary_union` before the population query — this eliminates all double-counting of people who live near multiple flares. The WorldPop raster is then masked with the union polygon and all population pixels within the area are summed.

### Updating

1. Add new flares to OpenStreetMap with tag `man_made=flare`
2. Open `population_impact.py` in Google Colab
3. Upload `irq_ppp_2020_UNadj_constrained.tif` to the Colab session
4. Run the script
5. Download the output `iraq_flaring_impact.json`
6. Commit it to the repo root
7. The website reads this file on load and updates the stat automatically

### Key result (October 2026)

| Metric | Value |
|---|---|
| Flares analysed | 437 |
| Impacted population | 5,181,870 |
| As % of Iraq population | 11.2% |
| Buffer radius | 5km |
| Raster resolution | ~100m per pixel |
| Iraq population reference | 2024 Census (46,118,793) |

---

## 6. Flare Activity Status — VIIRS Last Detection (`flare_viirs_status.json`)

**Source:** NASA FIRMS — VIIRS S-NPP thermal anomaly / active fire detections  
**API:** https://firms.modaps.eosdis.nasa.gov/api/area/ (Area API, CSV)  
**Products:** `VIIRS_SNPP_SP` (science-quality) + `VIIRS_SNPP_NRT` (near-real-time)  
**Window:** Trailing 365 days  
**Match radius:** 500 m  

### What it reports

For every mapped flare, this dataset records **the date it was last detected burning by satellite** and **how many times it was detected** over the past 12 months. It deliberately applies **no "active" / "inactive" label** — it reports only the verifiable fact. A flare with no detection in the window may be genuinely shut in (several Iraqi fields have been idled amid regional disruption), burning below VIIRS's detection threshold, or slightly mislocated in OpenStreetMap. Leaving the interpretation to the reader keeps the claim defensible.

### How it was generated

A VIIRS thermal detection is attributed to a flare when it falls within **500 m** of the mapped point, measured as great-circle (haversine) distance. 500 m was chosen after inspecting multiple Iraqi flares against VIIRS detections; a 1 km radius proved too wide and pulled in neighbouring stacks, while 500 m cleanly isolates individual flares.

The dataset is rebuilt **quarterly** via a Google Colab notebook that calls the FIRMS Area API directly (no manual download/upload). Because the Area API returns at most 5 days per request, the notebook steps through the 365-day window in 5-day chunks:

- **`VIIRS_SNPP_SP`** (science-quality) is pulled across the full window — the correct product for historical/archival analysis.
- **`VIIRS_SNPP_NRT`** tops up the most recent ~60 days, since SP processing lags by a month or two. Without this, the tail of the window would falsely show recently-active flares as "gone dark."
- The two products are merged and de-duplicated on `(lat, lon, acq_date)`.

Detections are binned into a ~0.01° spatial grid so each flare only compares against detections in its own and neighbouring cells, keeping the match fast across ~150,000 detections. For each flare the notebook records the most recent detection date and the total detection count in the window, then writes `flare_viirs_status.json` to the repo root.

```python
# Core match (simplified)
MATCH_RADIUS_M = 500
WINDOW_DAYS    = 365

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi   = math.radians(lat2 - lat1)
    dlmb   = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2
    return 2 * R * math.asin(math.sqrt(a))

for f in flares:
    last_date, count = None, 0
    for (lat, lon, d) in nearby_detections(f):           # grid-limited candidates
        if haversine_m(f['lat'], f['lon'], lat, lon) <= MATCH_RADIUS_M:
            count += 1
            if last_date is None or d > last_date:
                last_date = d
    status[str(f['id'])] = {
        'last_detection': last_date.isoformat() if last_date else None,
        'detections': count
    }
```

The flare list is read live from the repo's `query` file, so flare IDs always match the website exactly.

### Output structure

```json
{
  "_meta": {
    "generated": "2026-10-08",
    "window_days": 365,
    "match_radius_m": 500,
    "source": "NASA FIRMS VIIRS S-NPP (SP + NRT topup)",
    "bbox": "38.7,29.0,48.6,37.4",
    "flares": 437,
    "detections_in_window": 148485
  },
  "flares": {
    "13302378269": { "last_detection": "2026-10-07", "detections": 1207 },
    "13915525284": { "last_detection": null,         "detections": 0 }
  }
}
```

| Field | Description |
|---|---|
| `last_detection` | ISO date of the most recent VIIRS detection within 500 m, or `null` if none in the window |
| `detections` | Number of VIIRS detections attributed to the flare in the 365-day window |

### Visualisation

In each flare popup the map shows **"Last satellite detection"** (the date, or "none in last 12 months") and **"Satellite sightings (past year)"** (the detection count). On the map itself, flares **not** seen within the last 30 days carry a coloured ring around the orange dot — the dot colour is never changed, only a halo is added:

| Ring | Meaning (time since last detection) |
|---|---|
| Amber solid | 1–3 months |
| Red solid | 3–12 months |
| Grey dashed | No detection in the past 12 months |

Ring **thickness** is scaled to detection frequency (thin for sparse, thick for constant burners), so a flare that burned heavily then stopped reads as a bold ring — the signature of a shut-in rather than a marginal site.

### Updating

1. Open the VIIRS matcher notebook in Google Colab
2. Provide your FIRMS `MAP_KEY` (stored as a Colab Secret `FIRMS_MAP_KEY` after the first run)
3. Run all cells — the notebook pulls SP + NRT directly from the FIRMS API and performs the 500 m match
4. Download the generated `flare_viirs_status.json`
5. Commit it to the repo root
6. The website reads this file on load and populates the popup line and status rings automatically

### Key result (October 2026)

| Metric | Value |
|---|---|
| Flares analysed | 437 |
| Detections in window | 148,485 |
| Seen within last 30 days | 372 |
| Last seen > 90 days ago | 22 |
| No detection in 12 months | 34 |
| Match radius | 500 m |
| Window | 365 days |
| Source | NASA FIRMS VIIRS S-NPP (SP + NRT top-up) |
