# AEGIS Android apps (sideload)
Built from commit dfc7653 on 2026-11-20. Install by opening the .apk on the phone (allow "install unknown apps").
| file | what it is | needs internet? |
|---|---|---|
| AEGIS_SkyMap.apk | Sky Map: constellations, Messier, planets, AEGIS stars; uses location for your sky | telescope images only |
| AEGIS_Dashboard.apk | Toolkit dashboard; numbers frozen at build time (header shows code version) | no |
| Weave_Control.apk | Weave Control, OFFLINE SNAPSHOT: 144 precomputed engine states, only listed knob values | no |
| SarahsSky.apk | Sarah's Sky (separate app) | — |
Signing: a fixed sideload key (debug-grade, not for the Play Store). Builds made before 2026-11-20 used a different key: uninstall those once, then later updates install over the top.
