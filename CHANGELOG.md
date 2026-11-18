# Changelog

## 2026-11-18 (later)
- Repository reorganised into folders: datasets in `data/`, scripts and notebooks in `tools/`, screenshots in `images/`. The site, tracker, README, methodology and tools all point to the new paths. `carbon_mapper_query` and `worldpop_colab` gained a `.py` extension
- Old raw GitHub links to the data files (e.g. `…/main/query`) no longer work; use `…/main/data/query`. `Iraq Flaring Watch.jpeg` is now `images/iraq-flaring-watch-mobile.jpeg`, and `iraq-osm-flares-history.png` is in `images/`; the OSM diary post links were updated to match
- README: new Repository layout section; tracker page build 2026.11.18.a

## 2026-11-18
- **Night lights background replaced.** The 2012 NASA city-lights composite is gone. The Night background now shows NOAA-20 VIIRS Day/Night Band imagery (NASA GIBS) from the most recent night when the moon was down at the satellite's ~01:30 pass. The night is picked automatically from the lunar cycle, then checked against the imagery itself. The date is shown in the map attribution
- **Fixed: "homes powered" in the World Bank popup was overstated about 2.86×.** The 35% plant-efficiency factor had dropped out of the per-site formula again in the 2026-11-08 build; it is restored, so the popup now matches the national MW figure and `DATA_METHODOLOGY.md` (e.g. Kirkuk 200 M m³: ~175,673 → ~61,485 homes)
- VIIRS popup source now reads "Source: NASA FIRMS / VIIRS" (it still said "VIIRS SNPP" after the switch to NOAA-20/21)
- Docs refreshed: README (four data layers, data sources, formulas), `llms.txt`, `DATA_METHODOLOGY.md`, sitemap; README popup screenshot retaken with 2025 data
- Internal: sidebar element `stat-homes` renamed `stat-mw` (it holds the MW figure)

## 2026-11-13
- Fixed click-blocking: World Bank bubbles had their own full-screen canvas layer above the flares, so only the purple bubbles could be clicked. All circle layers (World Bank, plumes, VIIRS) now share one canvas, and flares sit on top
- Behaviour change: where a flare and a World Bank bubble overlap, the flare now wins the click

## 2026-11-08
- Live fire detections switched to NOAA-20 + NOAA-21 (VIIRS_SNPP_NRT stopped returning data). Both feeds are fetched in parallel, merged and de-duplicated

## 2026-10-17
- Restored the October homes-powered fix after it was lost in an intermediate build

## 2026-10-10
- Fixed: World Bank popup "homes powered" now applies the 35% plant efficiency, matching the national MW figure
- Reference labels and roads moved to their own non-clickable layer so they no longer block markers

## 2026-10-08
- Added **satellite activity status** for every mapped flare: last VIIRS detection date and number of detections over the past 12 months (`flare_viirs_status.json`, 500 m match radius, `iraq_flaring_viirs_match.ipynb`)
- Flares not detected recently get a coloured ring: amber (1–3 months), red (3–12 months), grey dashed (none in 12 months)
- Added EOX Sentinel-2 cloudless background
- Dark background switched to Esri Dark Gray Canvas (CARTO's free dark tiles were retired)
- Added `iraq_flare_tracker.json` and a test tracker page (`tracker.html`)

## 2026-10-05 – 2026-10-07
- Added **Sorani Kurdish** interface with full right-to-left layout; translations managed on Weblate (`locales/`), English is the source

## 2026-10-02
- Refreshed OSM flare snapshot (437 flares) and regenerated population figures: ~5.2 million Iraqis (5,181,870) within 5 km of a flare
- Refreshed Carbon Mapper Tanager plumes

## 2026-08-09
- Added **live fire detections** layer from NASA FIRMS VIIRS

## 2026-08-04
- Added first-visit guided tour

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
