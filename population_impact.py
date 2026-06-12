# ============================================================
# Iraq Flaring Watch — Population Impact Calculator
# Produces iraq_flaring_impact.json for iraqflaringwatch.com
#
# Requirements:
#   - irq_ppp_2020_UNadj_constrained.tif (WorldPop, uploaded to Colab)
#   - Internet access (fetches live flare data from GitHub)
#
# Methodology:
#   1. Fetch all active Iraq flare locations from OSM via GitHub
#   2. Buffer each flare by 5km in UTM Zone 38N (metric projection)
#   3. Union all buffers to eliminate double-counting
#   4. Mask WorldPop raster with union polygon
#   5. Sum population pixels within union area
#
# Data sources:
#   - Flare locations: OpenStreetMap (rawazrauf/iraq-flaring-watch)
#   - Population: WorldPop Project, Iraq 2020 UNadj constrained
#   - Iraq population: 2024 Census (46,118,793)
#   - Iraq households: 2024 Census (8,054,385)
#
# Author: Rawaz Rauf
# ============================================================

!pip install rasterio pyproj shapely requests numpy -q

import json
import numpy as np
import rasterio
import requests
from datetime import date
from rasterio.mask import mask
from shapely.geometry import Point, mapping
from shapely.ops import unary_union
from pyproj import Transformer

# ── Constants ────────────────────────────────────────────────
IRAQ_POPULATION = 46118793       # 2024 Census final results
IRAQ_HOUSEHOLDS = 8054385        # 2024 Census final results
BUFFER_RADIUS_M  = 5000          # 5km health risk threshold
UTM_CRS          = "EPSG:32638"  # UTM Zone 38N (Iraq)
WGS84_CRS        = "EPSG:4326"
WORLDPOP_FILE    = "irq_ppp_2020_UNadj_constrained.tif"
GITHUB_QUERY_URL = "https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/query"
OUTPUT_FILE      = "iraq_flaring_impact.json"

# ── Step 1: Fetch flare locations ────────────────────────────
print("Step 1: Fetching flare locations from GitHub...")
response = requests.get(GITHUB_QUERY_URL)
flare_data = response.json()

osm_date = "Unknown"
if flare_data.get("osm3s", {}).get("timestamp_osm_base"):
    osm_date = flare_data["osm3s"]["timestamp_osm_base"][:10]

coords = []
for el in flare_data["elements"]:
    lat = el.get("lat") or el.get("center", {}).get("lat")
    lon = el.get("lon") or el.get("center", {}).get("lon")
    if lat and lon:
        coords.append((float(lat), float(lon)))

print(f"  Loaded {len(coords)} flare locations (OSM snapshot: {osm_date})")

# ── Step 2: Build 5km circles in UTM Zone 38N ───────────────
print("Step 2: Building 5km buffers in UTM Zone 38N...")
to_utm = Transformer.from_crs(WGS84_CRS, UTM_CRS, always_xy=True)
to_wgs = Transformer.from_crs(UTM_CRS, WGS84_CRS, always_xy=True)

circles = []
for lat, lon in coords:
    x, y = to_utm.transform(lon, lat)
    circles.append(Point(x, y).buffer(BUFFER_RADIUS_M))

print(f"  Built {len(circles)} circles")

# ── Step 3: Union all circles ────────────────────────────────
print("Step 3: Computing union polygon (eliminates double-counting)...")
union_utm = unary_union(circles)
print(f"  Union type: {union_utm.geom_type}")

# Convert back to WGS84 for raster masking
def utm_to_wgs84_geojson(geom, transformer):
    if geom.geom_type == "Polygon":
        exterior = [transformer.transform(x, y) for x, y in geom.exterior.coords]
        return {"type": "Polygon", "coordinates": [[(lon, lat) for lon, lat in exterior]]}
    elif geom.geom_type == "MultiPolygon":
        polygons = []
        for poly in geom.geoms:
            exterior = [transformer.transform(x, y) for x, y in poly.exterior.coords]
            polygons.append([(lon, lat) for lon, lat in exterior])
        return {"type": "MultiPolygon", "coordinates": [[p] for p in polygons]}

union_wgs84 = utm_to_wgs84_geojson(union_utm, to_wgs)

# ── Step 4: Mask WorldPop raster ─────────────────────────────
print("Step 4: Extracting population from WorldPop raster...")
with rasterio.open(WORLDPOP_FILE) as src:
    out_image, _ = mask(src, [union_wgs84], crop=True)
    impacted_population = int(np.nansum(out_image[out_image > 0]))

impacted_pct = round(impacted_population / IRAQ_POPULATION * 100, 1)
print(f"  Impacted population: {impacted_population:,}")
print(f"  As % of Iraq population: {impacted_pct}%")

# ── Step 5: Write output JSON ────────────────────────────────
print("Step 5: Writing output file...")
output = {
    "generated": str(date.today()),
    "osm_snapshot": osm_date,
    "flare_count": len(coords),
    "iraq_population": IRAQ_POPULATION,
    "iraq_households": IRAQ_HOUSEHOLDS,
    "impacted_population": impacted_population,
    "impacted_pct": impacted_pct,
    "buffer_radius_km": 5,
    "methodology": "WorldPop 2020 UN-adjusted constrained raster (irq_ppp_2020_UNadj_constrained.tif). Each flare buffered by 5km in UTM Zone 38N (EPSG:32638). All buffers unioned to eliminate double-counting. Population summed from pixels within union area.",
    "data_sources": {
        "flares": "OpenStreetMap via rawazrauf/iraq-flaring-watch",
        "population_raster": "WorldPop Project, Iraq 2020 UNadj constrained (100m resolution)",
        "iraq_census": "Iraq Ministry of Planning, 2024 Census final results"
    }
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*50}")
print(f"OUTPUT: {OUTPUT_FILE}")
print(f"{'='*50}")
print(json.dumps(output, indent=2))
print(f"\nDone. Download {OUTPUT_FILE} and commit to your GitHub repo root.")
