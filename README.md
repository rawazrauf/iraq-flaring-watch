# 🔥 Iraq Flaring Watch

An open-source, serverless web map tracking gas flaring across Iraq — combining satellite detections, economic analysis, and community exposure data in a single interface.

**Live:** [iraqflaringwatch.com](https://iraqflaringwatch.com)

---

## What it shows 

Gas flaring burns off associated natural gas during oil extraction rather than capturing it. Iraq is one of the world's largest gas flaring nations. This tool makes that visible.

**Three data layers:**

- 🟠 **Active flare sites** — crowdsourced from OpenStreetMap, with population estimates for people living within 5km
- 🟣 **Economic waste** — World Bank GGFR 2025 volume estimates, sized by annual gas burned, with USD value lost and Iraqi homes that could have been powered
- 🔵 **Emission plumes** — verified CH₄ and CO₂ detections from Carbon Mapper's Tanager satellite, with emission rates in kg/hr

---

## Screenshots

### National Overview
All layers active — flare clusters, emission plumes, economic waste bubbles, and density heatmap across Iraq's oil fields.

![Iraq Flaring Watch national overview](https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/iraq-flaring-overview.jpg)

### Economic Waste — Wasted Gas Popup
Click any purple bubble to see annual gas volume, estimated USD value lost, and Iraqi homes that could have been powered.

![Wasted gas economic popup showing Basra Energy Company data](https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/emission-inspection-satellite.png)

### Active Flare Inspection
Zoom into any flare on satellite imagery to see population within 5km, coordinates, and direct links to Google Maps and OSM editor.

![Gas flare inspection popup on satellite imagery](https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/flare-inspection-satellite.png)

### Emission Plume — OpenStreetMap Background
CO₂ and CH₄ plumes detected by Carbon Mapper's Tanager satellite, shown with emission rate in kg/hr and satellite detection image.

![CO2 emission plume popup on OpenStreetMap background](https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/plume-inspection-OSM.png)

---

## Features

- **Satellite imagery** — Esri World Imagery, Esri Clarity Archive, NASA Black Marble night lights, dark canvas, and OpenStreetMap
- **Flare density heatmap** — visualise concentration across Iraq's oil fields
- **5km impact zone** — toggle safety radius buffers around each flare
- **Distance Analyzer** — geodesic ruler to measure proximity between any flare and a community
- **Share links** — every zoom, layer state, and background is encoded in the URL for instant sharing
- **Location finder** — jump to your current location to assess nearby flaring
- **Inspect Random Flare** — explore the dataset at random
- **Live OSM mode** — query the OpenStreetMap Overpass API in real time for latest data
- **One-click OSM editing** — direct link to iD editor to add or update flare data
- **National stats sidebar** — live economic and health impact statistics
- **Population impact layer** — 5.1 million Iraqis within 5km of a flare, calculated using WorldPop raster with non-overlapping union methodology
- **Shareable URLs** — every zoom, layer state, and background encoded in URL
- **Base map switcher** — accessible directly on map canvas for mobile users
- **Coordinate display** — shows lat/lon at zoom ≥ 13
- **Follow:** [@IraqFlaring](https://twitter.com/IraqFlaring) on X/Twitter

---

## Data sources

| Layer | Source | Coverage |
|---|---|---|
| Flare locations | [OpenStreetMap](https://www.openstreetmap.org) | Live / preloaded |
| Population (5km) | [WorldPop Project](https://www.worldpop.org) | 2020 UN-adjusted |
| Emission plumes | [Carbon Mapper / Tanager](https://carbonmapper.org) | 2024–2025 |
| Gas volumes & economics | [World Bank GGFR](https://www.worldbank.org/en/programs/gasflaringreduction/global-flaring-data) | 2012–2025 |
| Satellite imagery | Esri, NASA GIBS | Various |

---

## Economic methodology

Wasted gas value is estimated at **$3.50/MMBtu** (conservative global benchmark).

```
Value (USD) = vol_mm3 × 35,315 MMBtu/M m³ × $3.50 / 1,000,000
```

Electricity equivalent assumes **35% plant efficiency** and **5,000 kWh/household/year** (IEA 2024 × Iraq 2024 census, reviewed by Ahmed Gailani, Senior Energy Modeller at NESO).

---

## Self-hosting

Fully serverless — no backend required.

1. Fork this repository
2. Go to Settings → Pages → set source to `main`
3. Your instance will be live at `https://<username>.github.io/<repo>/`

For a custom domain, add a `CNAME` file to the repo root containing your domain name, then point your DNS A records to GitHub's IPs.

---

## Contributing

If a flare is missing from the map, add it to OpenStreetMap:

| Tag | Value |
|---|---|
| `man_made` | `flare` |

---

## Translations

Iraq Flaring Watch is being translated into Arabic and Sorani Kurdish by the community using [Weblate](https://weblate.org/), a libre web-based translation platform.

You can contribute translations — no coding required — at our Weblate project:
**[hosted.weblate.org/projects/iraq-flaring-watch](https://hosted.weblate.org/projects/iraq-flaring-watch/)**

Translation files live in the `locales/` directory (`en.json` is the source of truth). See [TRANSLATING.md](TRANSLATING.md) for contributor guidelines.

[![Translation status](https://hosted.weblate.org/widget/iraq-flaring-watch/svg-badge.svg)](https://hosted.weblate.org/engage/iraq-flaring-watch/)



## License & attributions

- Code: MIT License
- Map data: © OpenStreetMap contributors (ODbL)
- Population: WorldPop Project
- Basemaps: Esri, Earthstar Geographics, NASA GIBS
- Plumes: Carbon Mapper / Tanager
- Gas volumes: World Bank GGFR
- Translations: powered by [Weblate](https://weblate.org/) (libre hosting)

