# Sarah's Sky

Point your phone at the night sky and see the stars, planets and constellations drawn
right where they really are — plus a whole-sky map, the planets tonight, and world
sky-traditions (astrology/tarot shown honestly as *tradition, not astronomy*; the real
sky underneath is computed).

Everything runs on the phone. No account, no tracking, works offline.

## Two ways to use it

**1. Install the web app (quickest).**
Open the Pages link for this repo on an Android phone in Chrome, then menu → **Install app**
(or **Add to Home screen**). It lands on the home screen and runs full-screen and offline.
Tap **Point & See** for the AR camera sky.

**2. Install the APK.**
Every push builds a real Android app with GitHub Actions. Open the **Actions** tab → the
latest **Build Android APK** run → download the **SarahsSky-apk** artifact → unzip →
install `SarahsSky.apk` on the phone (allow "install from this source" once).

## What the sky shows
- 378 brightest stars in true positions and real colours, with names on the bright ones
- All 88 constellation figures
- Planets, the Moon and the Sun, computed live for your place and moment
- Pinch to zoom; tap anything for a plain-language card
- **Set North** — aim the ring at a star you know and tap it, to true-up the phone compass

The star map gets deeper and sharper over time as the AEGIS Gaia survey is processed —
`window.AR.updateCatalog(stars)` swaps in the richer list with no rebuild.

## Credits
Star & constellation data: Hipparcos / IAU names via d3-celestial (BSD-3-Clause).
Sky positions: Astronomy Engine (MIT). Built with care for Sarah.
