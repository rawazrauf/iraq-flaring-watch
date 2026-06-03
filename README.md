# 🗺️ Iraq Gas Flaring Watch — Powered by OpenStreetMap

An interactive, serverless web application designed to map, track, and measure gas flaring operations across Iraq. Built entirely on client-side technology, this platform empowers citizens, environmental researchers, and public advocates to analyze localized air quality risks using live crowdsourced data from OpenStreetMap (OSM) and high-resolution satellite imagery.

**Live Map Link:** [https://rawazrauf.github.io/iraq-flaring-watch/](https://rawazrauf.github.io/iraq-flaring-watch/)

---

## ✨ Key Features

### ⚡ Hybrid Data Engine

* **Static Preload:** Instantly displays pre-verified coordinates for major oil fields (Rumaila, Zubair, West Qurna, Majnoon, Halfaya, and Kirkuk) for zero-latency loading.
* **Live OSM Query:** Queries the live OpenStreetMap database in real-time via the public Overpass API to fetch the latest crowdsourced flaring nodes.
* **Intelligent Caching:** Hybrid architecture that caches population metrics to memory, ensuring lightning-fast performance while maintaining up-to-date regional data.

### 📊 Population Impact Analytics

* **Demographic Exposure:** Every flare stack now features integrated population density analysis powered by **@WorldPopProject**. Instantly estimate the number of people living within a 5km health-risk radius of any flare.

### 🛰️ Visualization & Analysis

* **Satellite Inspection:** Seamlessly switch to Esri World Imagery to inspect individual industrial flare stack structures at maximum zoom levels (up to magnification level 19).
* **Advanced Overlays:** Toggleable heatmaps for high-density identification, cluster views for regional analysis, and a 5km safety radius buffer.
* **Flaring Distance Analyzer:** A built-in geodesic ruler to evaluate localized exposure risk between flares and nearby communities.

### ✏️ Crowd-Sourced Editorial

* **Direct OSM Integration:** Features one-click deep links that redirect users to the OpenStreetMap iD editor, allowing volunteers to update flare metadata or add new sites instantly.

---

## 🔬 Scientific Context: The 5 km Threshold

The proximity tool evaluates safety limits using the standard geodesic distance formula on a sphere:

$$d = 2r \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)$$

Peer-reviewed environmental studies associate community proximity within **5 kilometers** of active industrial gas flares with an elevated risk of respiratory disease and heavy soot exposure. The app dynamically alerts users if a selected coordinate falls within this zone.

---

## 🚀 Quick Setup & Self-Hosting

This project is completely serverless and lightweight. To host it yourself:

1. Fork or Download this repository.
2. Go to **Settings -> Pages** in your GitHub repository.
3. Under **Build and deployment**, set the source branch to `main`.
4. Your map will be live at `https://<your-username>.github.io/<your-repo-name>/` within a minute.

---

## 🤝 How to Help Map Iraq

If you notice a flare is missing, add it to OpenStreetMap using this standard tags:

* **`man_made`**: `flare` (Identifies the structure)


---

📸 Application Previews

### 🌍 National Overview & Field Statistics
Visualize the density and distribution of gas flaring across all major Iraqi oil fields.

![National overview map of Iraq showing flare density](https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/iraq-flaring-overview.png)

### 🔥 High-Resolution Flare Inspection
Jump directly from nationwide statistics to inspecting individual emission points up close using high-resolution satellite imagery.

![Close-up inspection view of an active gas flare stack with metadata popup](https://raw.githubusercontent.com/rawazrauf/iraq-flaring-watch/main/flare-inspection-satellite.png)


---

## ⚖️ License and Attributions

* **Code:** Distributed under the MIT License.
* **Map Data:** OpenStreetMap contributors, licensed under the Open Database License (ODbL).
* **Analytics:** Population data provided by the [WorldPop Project](https://www.worldpop.org/).
* **Basemaps:** Satellite tiles courtesy of Esri, Earthstar Geographics, and NASA.
