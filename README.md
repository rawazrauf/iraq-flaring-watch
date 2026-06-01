🗺️ Iraq Gas Flaring Watch — Powered by OpenStreetMap

An interactive, serverless web application designed to map, track, and measure gas flaring operations across Iraq. Built entirely on client-side technology, this platform empowers citizens, environmental researchers, and public advocates to analyze localized air quality risks using live crowdsourced data from OpenStreetMap (OSM) and high-resolution Esri Satellite imagery.

✨ Key Features

⚡ Double-Engine Data Architecture:

Static Preload: Instantly displays pre-verified coordinates for major oil fields (Rumaila, Zubair, West Qurna, Majnoon, Halfaya, and Kirkuk).

Live OSM Query: Queries the live OpenStreetMap database in real-time via the public Overpass API to fetch the latest crowdsourced flaring nodes.

🛰️ High-Resolution Satellite Overlay: Seamlessly switch to Esri World Imagery to inspect individual industrial flare stack structures at maximum zoom levels (up to magnification level 18).

🔴 Advanced Data Visualizations: Interactive marker clustering, heatmaps to identify high-density flaring hubs, and a togglable 5km safety radius overlay.

📍 Flaring Distance Analyzer: A built-in geodesic ruler using the Haversine mathematical model. Select any flare stack on the map, click on nearby communities, and instantly evaluate exposure risk.

✏️ Crowd-Sourced Editorial Links: Includes one-click deep links that redirect users to the OpenStreetMap iD editor for specific coordinates, allowing volunteers to update metadata instantly.

🚀 Quick Setup & Self-Hosting

This project is completely serverless and lightweight. To host it yourself on GitHub Pages for free:

Fork or Download this repository.

Ensure your main map file is named index.html.

Go to Settings -> Pages in your GitHub repository.

Under Build and deployment, set the source branch to main (or master) and click Save.

Your map will be live at https://<your-username>.github.io/<your-repo-name>/ within a minute!

🔬 How the Proximity Analyzer Works

The proximity tool evaluates safety limits using the standard geodesic distance formula on a sphere:

$$d = 2r \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)$$

Where:

$\phi_1, \phi_2$ are the latitudes of the two points (in radians).

$\Delta \phi$ is the difference in latitude.

$\Delta \lambda$ is the difference in longitude.

$r$ is the Earth's radius ($6,371 \text{ km}$).

Why $5 \text{ km}$? Peer-reviewed environmental studies associate community proximity within 5 kilometers of active industrial gas flares with an elevated risk of cancer, respiratory disease, and heavy soot exposure. The app dynamically alerts users with a warning color if their selected point falls within this zone.

## 🤝 How to Help Map Iraq on OpenStreetMap

If you notice a flare is missing, you can add it directly to OpenStreetMap using these standard tags:

*   **man_made**: `flare` — Identifies the structure as an active gas flare.
*   **operator**: [Company Name] — The oil company currently operating the field or facility.
*   **field**: [Field Name] — The geographical name of the oil/gas field.


## 📸 Application Previews

### 🌍 National Overview & Field Statistics
Visualize the density and distribution of gas flaring across all major Iraqi oil fields.

![National overview map of Iraq showing flare density](https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/iraq-flaring-overview.png)

### 🔥 High-Resolution Flare Inspection
Jump directly from nationwide statistics to inspecting individual emission points up close using high-resolution satellite imagery.

![Close-up inspection view of an active gas flare stack with metadata popup](https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/flare-inspection-satellite.png)


⚖️ License and Attributions

Code: Distributed under the MIT License. Feel free to copy, modify, and host.

Map Data: OpenStreetMap contributors, licensed under the Open Database License (ODbL).

Basemaps: Satellite tiles courtesy of Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community.
