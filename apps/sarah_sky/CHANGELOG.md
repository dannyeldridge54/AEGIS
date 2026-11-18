# Changelog
## 1.6.2 — 18 Nov 2026
- Tarot: five more decks — Constellations, Spiral Galaxy, Neon Sign, Cyber Circuit, Neon Horizon (ten in all). Card art is now kept inside the card frame; Neon Horizon's sun shows one stripe per card number.

## 1.6.1 — 18 Nov 2026
- Tarot: five deck styles in the Janus palette — Mirror Lattice, Orbitals, Feynman Paths, Sacred Geometry, Symmetry Rosette. Pick one under Readings → Tarot → Deck; the choice is remembered and the open spread redraws in the new deck.

## 1.6.0 — 18 Nov 2026
- Compare two people (synastry): pick any saved chart under a cast chart to see the aspects between the two charts, each in plain words, and an overall tone.
- Tarot: every Minor Arcana card now has its own upright and reversed meaning (all 56), not a suit formula.
- Point & See shows the field of view and magnification (×1 = the starting view).
- Search is never silent: offline it says the name lookup needs the internet; online it says "Not found" after 6 seconds if the lookup does not answer.
- Map zoom buttons lifted off the bottom bar on phones.
## 1.5.1 — 18 Nov 2026
- Point & See: pinch zoom rebuilt on pointer events (works the same on Android, iPhone and desktop), wider zoom range (90° to 2°, even steps), double-tap to zoom in, zoom remembered; Lock shows "Unlock" while locked, the locked view stays still while the phone moves, one finger looks around, and unlocking returns to the phone without a slide.
- The Point & See button hides while any sheet is open; on small phones "Bigger text" moves into More so the top bar stays one row.
## 1.5.0 — 18 Nov 2026
- Phone navigation: a bottom tab bar (Sky · Tonight · Signs · Readings · More) like a native app; panels open as bottom sheets; a "More" sheet for Layers, Tour, Learn, AEGIS stars, Point & See, Tarot and About.
- The Android back button now closes whatever is open (panel, readings, signs, More) instead of leaving the app.
- Safe-area padding for phones with notches and gesture bars.
## 1.4.1 — 18 Nov 2026
- Birth chart now ends with "Today's sky on this chart": the real planets today against the natal chart (transits to every planet, the Ascendant and the Midheaven, tight orbs, slow planets first) and the house the Moon is passing through.
- Numerology: life-path number (with master numbers 11, 22, 33) and its meaning.
## 1.4.0 — 18 Nov 2026
- Readings: full birth chart — Sun, Moon, Mercury to Pluto (with retrogrades), Ascendant and Midheaven from the real sky (true ecliptic of date); Placidus, Whole-sign or Equal houses; Tropical or Sidereal (Lahiri); aspects with orbs; element and modality balance; a chart wheel; and a written reading for every placement. Time zone history handled through the time-zone database (or local mean time for old births); birthplace lookup; charts saved on the device. Checked against Einstein's published chart (14 Mar 1879, 11:30 LMT, Ulm): Sun 23°30' Pisces, Moon 14°32' Sagittarius, Ascendant 11°39' Cancer, MC 12°50' Pisces — all match.
- Tarot spreads: one card, Past–Present–Future, Mind–Body–Spirit and the 10-card Celtic Cross, shuffled with the device's secure random generator, with position meanings and a Major Arcana count.
## 1.3.3 — 18 Nov 2026
- New tradition: Maya calendar — Tzolk'in day sign, Haab' date and Long Count (GMT correlation 584283; checked: 21 Dec 2012 = 13.0.0.0.0 4 Ajaw 3 K'ank'in).
- One-time AR accuracy tip.

## 1.3.2 — 18 Nov 2026
- Android app: the app is now served inside the app over https (WebViewAssetLoader) instead of file://. On file:// the phone blocked the main script and the data files, which is why most buttons did nothing. Search, tabs, Tonight, Tour, Learn, AEGIS stars and the star data now load in the app.
- The app only reloads after permissions if one was actually granted.
## 1.3.1 — 18 Nov 2026
- Point & See accuracy: on Android the compass-referenced sensor stream is now used and the drifting relative stream is ignored once it appears (they were overwriting each other); on iPhone the gyro is tied to the compass heading; motion is smoothed to stop the jitter; sensors now start even on browsers that expose a permission prompt.
- Set North (tap the Sun, Moon, a planet or a bright star) is remembered between sessions, which also corrects magnetic declination.
- Location: best GPS fix within ~12 s (shows its accuracy), remembered for next time; a clear notice if it falls back to Oklahoma City.
- Floating buttons hide while a panel is open; Point & See moved below the map toolbar.
## 1.3.0 — 18 Nov 2026
- Opening screen: "Philosophia — for Sarah", a turning zodiac wheel, flower of life, star and planet symbols while the map loads — when loading finishes "Philosophia" flips to "for Sarah", the wheel spins up and the screen zooms open into the sky (tap to skip; calm version with reduced motion).
- Janus "Prismatic Light" colours; dark by default (a light theme stays available).
- Overlays & tools panel is now a button that opens on tap, so it no longer covers the map on phones.
- Working traditions (each labelled as tradition, not astronomy, from real Sun/Moon positions): Western zodiac; Vedic nakshatra, pada, rashi and tithi (Lahiri ayanamsa); Chinese calendar year animal, element, stem-branch and lunar date; Moon phase, illumination, age, sign and next full/new moon; daily tarot card (same card all day) with extra draws.
- Choices remembered on the device; nothing leaves it.
## 1.1.0 — 15 Nov 2026
- AEGIS discovery categories layer (seven categories from the Star Mapper, rules locked in PREREG_D716), with counts and toggles.
- Combined classroom review tallies shown on each star; Gaia source_id search; star cards show 3D motion and true brightness.
- Survey coverage drawn as tile markers (the MOC renderer crashed in testing).
- Default port 8780, so the map and the Star Mapper monitor (8765) can run side by side; the monitor also serves the map at /skymap.
## 1.0.0 — 15 Nov 2026
- First release: Aladin Lite sky with 8 surveys, constellations, named stars, Messier objects, planets, Tonight, tour, lessons, AEGIS flags and reviews, PWA, launchers.
