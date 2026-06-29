# Changelog

## 2026-06-29
- Updated OSM flare dataset — new flare locations added from latest Overpass snapshot (June 29, 2026)
- Regenerated `query_population.json` and `iraq_flaring_impact.json` to reflect new flares

## 2026-06-27
- Upgraded to World Bank GGFR 2025 data — all economic waste figures now reflect 2025 volumes
- Updated national flaring total to ~24 BCM (up from ~18 BCM in 2024 dataset)
- Added `iraq_wb_flares_all_years.json` covering 2012–2025

## 2026-06-25
- Added Twitter/X follow button (@IraqFlaring) to header and About popup
- Changed default background to OpenStreetMap
- Changed default view to zoom 6.0 centred on Iraq

## 2026-06-12
- Added national stats sidebar: Gas Value Wasted, Annual Flaring Volume, Electricity Generation Potential, People Within 5km
- Added `iraq_flaring_impact.json` — non-overlapping population impact calculation using WorldPop union polygon methodology (~5.1M Iraqis within 5km of a flare)
- Added `population_impact.py` script for reproducible population impact calculations
- Gas price basis updated to $3.50/MMBtu per Iraqi Cabinet Session 49 (2025) official pricing
- Household electricity consumption updated to 5,000 kWh/yr based on IEA 2024 × Iraq 2024 census (reviewed by Ahmed Gailani, Senior Energy Modeller, NESO)
- Sidebar scrolls as single unified panel on mobile
- Pre-load World Bank data silently on page start for instant stats

## 2026-06-09
- Migrated heatmap from leaflet.heat to heatmap.js — fixed zoom animation offset bug
- Added Background control on map canvas (top-left) with radio buttons — accessible on mobile without opening sidebar
- Removed Base Satellite section from sidebar
- Added simulated popup on shared link load — opens nearest marker to hash coordinates automatically
- Hash URL now encodes background layer (e.g. `/satellite`, `/streets`)
- Live OSM query upgraded to Promise.any race pattern across three Overpass endpoints — load time reduced from ~60s to ~5s
- Restored dynamic WorldPop API population lookup for new flares in Live OSM mode
- Consolidated moveend/zoomend event listeners
- Removed zombie variables (`wbFlareData`, `currentDataSource`)

## 2026-06-08
- Added World Bank GGFR 2024 economic waste layer (purple bubbles)
- Added Carbon Mapper Tanager emission plumes layer (cyan dots)
- Added collapsible map legend as Leaflet native control
- Added floating Layers and Background controls on map canvas
- Added shareable URLs encoding zoom, layers, and background
- Added coordinate display at zoom ≥ 13
- Added locate me button
- Launched custom domain iraqflaringwatch.com
- Major UX overhaul

## 2026-06-04
- Refined OSM flare dataset — filtered noise to pinpoint actual flare locations
- Integrated WorldPop population analysis — population within 5km of every flare
- Mobile and web support for population layer

## 2026-06-01
- Initial release
- OSM flare locations with heatmap
- Distance Analyzer — geodesic ruler to measure proximity between flares and communities
