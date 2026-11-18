# Installing the AEGIS Sky Map

The app is a folder of static files. Pick whichever fits your school.

## 1. One computer (teacher's laptop, projector PC)
1. Download and unzip `aegis-skymap-1.0.0.zip` (or this folder).
2. Windows: double-click **START_SKY_MAP.bat**. Mac/Linux: run `sh start_sky_map.sh`.
3. The map opens in your browser at `http://localhost:8780`. Close the black window to stop it.

Needs Python 3 (free from python.org; on Windows tick "Add Python to PATH"). Opening `index.html` directly from the
file system will not work, because browsers block modules on `file://` pages.

## 2. A classroom on the same network
Run `START_SKY_MAP.bat --lan` (or `sh start_sky_map.sh --lan`). It prints an address like `http://192.168.1.20:8780/index.html`
that students' devices can open while the teacher's computer is on. Your network must allow devices to reach each other.

## 3. The whole school or district (recommended)
Copy the folder to any web server: the school website, an intranet server, Netlify, Cloudflare Pages or GitHub Pages.
No server code, database or configuration is needed; serve the files as they are, over HTTPS.
- **GitHub Pages:** in the repository settings, Pages → deploy from branch, folder `/apps/skymap`. (Not switched on yet: it publishes
  the map publicly, so it's the project owner's decision.)
- Students can then **install it as an app** from the browser menu (Chrome/Edge: "Install AEGIS Sky Map"; iPad/iPhone Safari:
  Share → Add to Home Screen). Installed, it opens like an app and works offline, apart from the telescope pictures.

## Network requirements
Allow HTTPS to `alasky.cds.unistra.fr` and `alaskybis.cds.unistra.fr` (telescope images). Optional: `simbad.cds.unistra.fr`
(the "Look up in SIMBAD" link and name search for objects not in the built-in list).
No other external requests are made. No cookies, analytics or accounts.

## Devices
Any browser with WebGL 2: current Chrome, Edge, Firefox and Safari (iPadOS 15+), and Chromebooks. Very old devices may show
a "needs WebGL 2" notice; the Tonight, Tour and Learn panels still work there.

## Privacy (for data-protection officers)
The app stores three things in the browser only: display settings, an optional location (if a user types it or allows
location access, used only to compute what is above the horizon), and review votes. Nothing is sent anywhere. Clearing the
browser's site data removes them.

## Updating the AEGIS data
On the Star Mapper computer run `ufe-v2/START_MAP_FEED.bat` (or `python -m aegis.map_feed` in `ufe-v2/`). It refreshes all four
AEGIS files in `data/` (coverage, flags, discoveries, review tallies) and takes in any class review CSVs placed in
`ufe-v2/cosmos_map/reviews_in/`. Then copy the `data/` folder to wherever the map is hosted.
