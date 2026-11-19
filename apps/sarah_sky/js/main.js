// AEGIS Sky Map — main module. Aladin Lite v3 (LGPL-3, CDS) draws the sky; astronomy-engine (MIT) computes planets.
import A from "../vendor/aladin.js";
import { SURVEYS, TOUR, LESSONS, ACTIVITIES } from "./content.js";

const $ = (s, el = document) => el.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const store = {
  get(k, d) { try { const v = localStorage.getItem("aegis-skymap:" + k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("aegis-skymap:" + k, JSON.stringify(v)); } catch {} },
};
const fmtRA = (deg) => { const h = ((deg % 360) + 360) % 360 / 15; const hh = Math.floor(h), mm = Math.floor((h - hh) * 60), ss = ((h - hh) * 60 - mm) * 60; return `${hh}h ${String(mm).padStart(2, "0")}m ${ss.toFixed(0).padStart(2, "0")}s`; };
const fmtDec = (d) => { const s = d < 0 ? "−" : "+"; d = Math.abs(d); const dd = Math.floor(d), mm = Math.floor((d - dd) * 60); return `${s}${dd}° ${String(mm).padStart(2, "0")}′`; };

const state = {
  aladin: null, layers: {}, data: {}, survey: store.get("survey", SURVEYS[0].id),
  visible: store.get("visible", { constellations: true, conNames: true, stars: true, messier: true, planets: true, aegis: true, coverage: false }),
  location: store.get("location", null), when: null, tourStep: 0, reviews: store.get("reviews", {}),
};

async function loadJSON(path) { try { const r = await fetch(path); if (!r.ok) throw 0; return await r.json(); } catch { return null; } }

// ---------- sky ----------
async function initSky() {
  try { await A.init; } catch (e) { $("#fallback").hidden = false; return false; }
  state.aladin = A.aladin("#sky", {
    survey: state.survey, fov: 220, target: "266.4168 -29.0078", projection: "AIT", cooFrame: "ICRSd",
    showReticle: false, showZoomControl: true, showFullscreenControl: true, showLayersControl: true, showGotoControl: false,
    showCooGridControl: true, showSimbadPointerControl: true, showFrame: true, showCooLocation: true, showShareControl: false,
    showContextMenu: true, showSettingsControl: true,
  });
  state.aladin.on("objectClicked", (obj) => { if (obj && obj.data) showInfo(obj.data); });
  let last = 0; state.aladin.on("zoomChanged", () => { const now = Date.now(); if (now - last > 150) { last = now; applyVisibility(); } });
  return true;
}

function setSurvey(id) {
  state.survey = id; store.set("survey", id);
  const al = state.aladin; if (!al) return;
  try { if (al.setImageSurvey) al.setImageSurvey(id); else al.setBaseImageLayer(al.newImageSurvey(id)); } catch (e) { console.warn("survey", e); }
}

function catalog(name, color, opts = {}) {
  const c = A.catalog({ name, color, sourceSize: opts.size ?? 10, shape: opts.shape ?? "circle", displayLabel: !!opts.label,
    labelColumn: "label", labelColor: opts.labelColor ?? color, labelFont: opts.font ?? "13px sans-serif" });
  state.aladin.addCatalog(c); return c;
}

function buildLayers() {
  const al = state.aladin, D = state.data, L = state.layers;
  if (D.cons) {
    L.constellations = A.graphicOverlay({ color: "#5d7bd6", lineWidth: 1.2, name: "Constellation lines" });
    al.addOverlay(L.constellations);
    for (const c of D.cons.constellations) for (const seg of c.lines) {
      // split segments crossing RA = 0/360 so the polyline does not wrap the long way round
      let cur = [seg[0]];
      for (let i = 1; i < seg.length; i++) { if (Math.abs(seg[i][0] - seg[i - 1][0]) > 180) { if (cur.length > 1) L.constellations.add(A.polyline(cur)); cur = []; } cur.push(seg[i]); }
      if (cur.length > 1) L.constellations.add(A.polyline(cur));
    }
    L.conNames = catalog("Constellation names", "rgba(143,166,255,0.01)", { size: 6, label: true, labelColor: "#8fa6ff", font: "14px sans-serif" });
    L.conNames.addSources(D.cons.constellations.map((c) => A.source(c.label[0], c.label[1], { kind: "constellation", ...c, pos: c.label, label: c.name, lines: undefined })));
  }
  if (D.stars) {
    L.stars = catalog("Named stars", "#ffe9a8", { size: 7, label: true, font: "12px sans-serif", shape: "circle" });
    L.stars.addSources(D.stars.stars.map((s) => A.source(s.ra, s.dec, { kind: "star", label: s.name, ...s })));
    L.starsBright = catalog("Brightest stars", "#ffe9a8", { size: 8, label: true, font: "12px sans-serif", shape: "circle" });
    L.starsBright.addSources(D.stars.stars.filter((s) => s.mag < 1.0).map((s) => A.source(s.ra, s.dec, { kind: "star", label: s.name, ...s })));
  }
  if (D.messier) {
    L.messier = catalog("Messier objects", "#4cc3ff", { size: 12, label: true, shape: "square" });
    L.messier.addSources(D.messier.objects.map((m) => A.source(m.ra, m.dec, { kind: "messier", label: m.id + (m.common ? " " + m.common : ""), ...m })));
    L.messierDots = catalog("Messier objects (markers)", "#4cc3ff", { size: 8, shape: "square" });
    L.messierDots.addSources(D.messier.objects.map((m) => A.source(m.ra, m.dec, { kind: "messier", label: m.id, ...m })));
  }
  L.planets = catalog("Sun, Moon and planets (now)", "#ff6ec7", { size: 14, label: true, shape: "circle", font: "bold 13px sans-serif" });
  updatePlanetLayer();
  if (D.flags && D.flags.stars && D.flags.stars.length) addFlagLayers(D.flags);
  if (D.disc && D.disc.stars) addDiscoveryLayers(D.disc);
  if (D.coverage && Array.isArray(D.coverage.tile_centres) && D.coverage.tile_centres.length) {
    // one faint marker per finished survey tile (about 3.4 square degrees each)
    L.coverage = catalog("AEGIS survey coverage", "rgba(111,209,139,0.55)", { size: 6, shape: "square" });
    const n = D.coverage.tiles || [];
    L.coverage.addSources(D.coverage.tile_centres.map((c, i) => A.source(c[0], c[1], { kind: "tile", label: "", ra: c[0], dec: c[1], tile: n[i]?.[0], stars: n[i]?.[1] })));
  }
  applyVisibility();
}

const FLAG_COLORS = { high_velocity: "#ff3d8b", distance_mismatch: "#d43cff", astrometric_excess: "#c58bff" };
const FLAG_LABELS = { high_velocity: "High velocity", distance_mismatch: "Distance mismatch", astrometric_excess: "Wobbly fit (RUWE > 1.4)" };
function addDiscoveryLayers(disc) {
  const L = state.layers; L.disc = L.disc || {};
  for (const [k, meta] of Object.entries(disc.categories || {})) {
    const list = disc.stars[k] || []; if (!list.length || L.disc[k]) continue;
    const c = catalog("Discoveries: " + meta.label, meta.color, { size: 7, shape: "rhomb" });
    c.addSources(list.map((st) => A.source(st.ra, st.dec, { kind: "aegis", label: "", ...st, cats: [k] })));
    L.disc[k] = c;
  }
}
function addFlagLayers(flags) {
  const L = state.layers; L.aegis = L.aegis || {};
  for (const [k, color] of Object.entries(FLAG_COLORS)) {
    if (L.aegis[k]) continue;
    const c = catalog("AEGIS: " + (flags.criteria?.[k]?.label || FLAG_LABELS[k]), color, { size: 8, shape: "cross" });
    const primary = (s) => ["high_velocity", "distance_mismatch", "astrometric_excess"].find((f) => s.flags.includes(f));
    c.addSources(flags.stars.filter((s) => primary(s) === k).map((s) => A.source(s.ra, s.dec, { kind: "aegis", label: "", ...s })));
    L.aegis[k] = c;
  }
}

function setShown(layer, on) { if (!layer) return; try { on ? layer.show() : layer.hide(); } catch {} }
function applyVisibility() {
  const v = state.visible, L = state.layers;
  let fov = 180; try { fov = state.aladin.getFov()[0]; } catch {}
  const wide = fov > 90;           // declutter: fewer labels when the whole sky is shown
  setShown(L.constellations, v.constellations); setShown(L.conNames, v.conNames);
  setShown(L.stars, v.stars && !wide); setShown(L.starsBright, v.stars && wide);
  setShown(L.messier, v.messier && fov < 60); setShown(L.messierDots, v.messier && fov >= 60); setShown(L.planets, v.planets); setShown(L.coverage, v.coverage);
  if (L.aegis) for (const c of Object.values(L.aegis)) setShown(c, v.aegis);
  if (L.disc) for (const [k, c] of Object.entries(L.disc)) setShown(c, v["disc_" + k] !== false);
  store.set("visible", v);
}

// ---------- solar system ----------
const BODIES = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"];
function bodyPositions(date) {
  const AE = window.Astronomy; if (!AE) return [];
  const loc = state.location || { lat: 0, lon: 0 };
  const obs = new AE.Observer(loc.lat, loc.lon, 0), t = AE.MakeTime(date);
  return BODIES.map((b) => {
    const j2000 = AE.Equator(b, t, obs, false, true), ofdate = AE.Equator(b, t, obs, true, true);
    const hor = AE.Horizon(t, obs, ofdate.ra, ofdate.dec, "normal");
    let mag = null; try { if (b !== "Sun") mag = AE.Illumination(b, t).mag; } catch {}
    let rise = null, set = null;
    if (state.location) { try { rise = AE.SearchRiseSet(b, obs, +1, t, 1)?.date; set = AE.SearchRiseSet(b, obs, -1, t, 1)?.date; } catch {} }
    return { name: b, ra: j2000.ra * 15, dec: j2000.dec, alt: hor.altitude, az: hor.azimuth, mag, rise, set, dist_au: j2000.dist };
  });
}
function updatePlanetLayer() {
  const L = state.layers; if (!L.planets) return;
  try { L.planets.removeAll(); } catch {}
  const when = state.when || new Date();
  L.planets.addSources(bodyPositions(when).map((p) => A.source(p.ra, p.dec, { kind: "planet", label: p.name, ...p, when: when.toISOString() })));
}

// ---------- info card ----------
function goto(ra, dec, fov) { const al = state.aladin; if (!al) return; al.gotoRaDec(ra, dec); if (fov) al.setFoV(fov); setTimeout(applyVisibility, 50); }
function showInfo(d) {
  const pos = `RA ${fmtRA(d.ra)} · Dec ${fmtDec(d.dec)}`;
  let h = "";
  if (d.kind === "constellation") h = `<h3>${esc(d.name)}</h3><p class="muted">Constellation · ${esc(d.latin)} (${esc(d.id)})</p><p>Constellations are 88 official areas of the sky. The lines join its brighter stars into the traditional figure.</p>`;
  else if (d.kind === "star") h = `<h3>${esc(d.name)}</h3><p class="muted">Star · ${esc(d.desig)} · HIP ${esc(d.hip)}</p><p>Brightness (magnitude): <b>${d.mag}</b>${d.mag < 1 ? " — one of the brightest stars in the sky" : ""}. Smaller numbers are brighter.</p>`;
  else if (d.kind === "messier") h = `<h3>${esc(d.id)}${d.common ? " · " + esc(d.common) : ""}</h3><p class="muted">${esc(d.type)} · ${esc(d.ngc)}</p><p>Magnitude ${d.mag ?? "?"}. Charles Messier listed these fuzzy objects in the 1700s so comet hunters would not mistake them for comets.</p>`;
  else if (d.kind === "planet") {
    const up = state.location ? (d.alt > 0 ? `<span class="up">above the horizon</span> (altitude ${d.alt.toFixed(0)}°)` : `<span class="down">below the horizon</span>`) : `<span class="muted">set your location in Tonight to see if it is up</span>`;
    h = `<h3>${esc(d.name)}</h3><p class="muted">Position at ${esc(new Date(d.when).toLocaleString())}</p><p>Now ${up}.</p>${d.mag != null ? `<p>Magnitude ${d.mag.toFixed(1)}.</p>` : ""}<p class="muted">Planets move against the stars from night to night; that is why the Greeks called them "wanderers".</p>`;
  } else if (d.kind === "aegis") h = aegisInfo(d);
  else if (d.kind === "tile") h = `<h3>AEGIS survey tile ${esc(d.tile)}</h3><p>${(d.stars ?? 0).toLocaleString()} Gaia stars in this patch of sky (about 3.4 square degrees), every one counted again against ESA's archive.</p>`;
  else h = `<h3>${esc(d.label || "Object")}</h3>`;
  h += `<p class="muted">${pos}</p><p><button class="btn ghost" id="zoomHere">Zoom here</button> <a class="btn ghost" target="_blank" rel="noopener" href="https://simbad.cds.unistra.fr/simbad/sim-coo?Coord=${d.ra}+${d.dec}&Radius=${d.kind === "aegis" ? 2 : 30}&Radius.unit=arcsec">Look up in SIMBAD</a></p>`;
  $("#infoBody").innerHTML = h; $("#info").hidden = false;
  $("#zoomHere").onclick = () => goto(d.ra, d.dec, d.kind === "aegis" ? 0.05 : d.kind === "constellation" ? 30 : 1);
  if (d.kind === "aegis") wireVote(d);
}
function aegisInfo(s) {
  const C = state.data.flags?.criteria || {}, K = state.data.disc?.categories || {};
  const cats = (s.cats || []).map((k) => `<li><b>${esc(K[k]?.label || k)}</b> (${esc(K[k]?.rule || "")}): ${esc(K[k]?.why || "")}</li>`).join("");
  const t = state.data.reviewsAll?.stars?.[s.id];
  const tally = t ? `<p>Reviews collected so far: <b>${t.real}</b> looks real · <b>${t.artefact}</b> artefact · ${t.unsure} not sure.</p>` : "";
  const crit = (s.flags || []).map((f) => `<li><b>${esc(C[f]?.label || f)}</b> (${esc(C[f]?.rule || "")}): ${esc(C[f]?.meaning || "")} <span class="muted">To confirm: ${esc(C[f]?.confirm || "")}</span></li>`).join("");
  const v = state.reviews[s.id]?.vote;
  return `<h3>Gaia DR3 ${esc(s.id)}</h3><p class="muted">${s.cats ? "AEGIS discovery category" : "AEGIS flagged star"} · candidate, not a discovery${s.confirmed ? " · passed AEGIS quality checks" : ""}</p>
  <table><tr><td>G magnitude</td><td>${s.g?.toFixed?.(2) ?? "–"}</td></tr><tr><td>Colour BP−RP</td><td>${s.bp_rp?.toFixed?.(2) ?? "–"}</td></tr>
  <tr><td>Distance</td><td>${s.dist_pc ? Math.round(s.dist_pc).toLocaleString() + " parsecs (" + Math.round(s.dist_pc * 3.2616).toLocaleString() + " light-years)" : "–"}</td></tr>
  <tr><td>Speed across the sky</td><td>${s.vtan ? Math.round(s.vtan) + " km/s" : "–"}</td></tr>${s.rv != null ? `<tr><td>Speed towards/away from us</td><td>${Math.round(s.rv)} km/s</td></tr>` : ""}
  ${s.pm_mas_yr ? `<tr><td>Motion across the sky</td><td>${(s.pm_mas_yr / 1000).toFixed(2)} arcsec per year</td></tr>` : ""}${s.abs_g != null ? `<tr><td>True brightness (abs. mag.)</td><td>${s.abs_g}</td></tr>` : ""}
  <tr><td>RUWE</td><td>${s.ruwe?.toFixed?.(2) ?? "–"}</td></tr></table>
  <ul>${cats}${crit}</ul>${s.note ? `<p class="muted">${esc(s.note)}</p>` : ""}${tally}
  <p><b>Your review</b> (saved only on this device):</p><div class="vote" id="vote">
  ${["looks real", "looks like an artefact", "not sure"].map((x) => `<button data-v="${x}" aria-pressed="${v === x}">${x}</button>`).join("")}</div>
  <p><a target="_blank" rel="noopener" href="https://gea.esac.esa.int/archive/">Gaia archive</a> · source_id ${esc(s.id)}</p>`;
}
function wireVote(s) {
  for (const b of document.querySelectorAll("#vote button")) b.onclick = () => {
    state.reviews[s.id] = { vote: b.dataset.v, t: new Date().toISOString(), flags: [...(s.cats || []), ...(s.flags || [])].join(";"), ra: s.ra, dec: s.dec };
    store.set("reviews", state.reviews);
    for (const o of document.querySelectorAll("#vote button")) o.setAttribute("aria-pressed", String(o === b));
  };
}

// ---------- panels ----------
function discRows() {
  const D = state.data.disc; if (!D || !D.categories || !Object.values(D.stars || {}).some((l) => l.length)) return "";
  return `<h3>AEGIS discoveries (candidates)</h3>` + Object.entries(D.categories).map(([k, m]) =>
    `<label class="row"><input type="checkbox" data-disc="${k}" ${state.visible["disc_" + k] !== false ? "checked" : ""}><span class="sw" style="background:${m.color}"></span>${esc(m.label)} <span class="muted">(${(D.counts?.[k] ?? 0).toLocaleString()})</span></label>`).join("");
}
const PANELS = {
  layers() {
    const v = state.visible, row = (k, label, color) => `<label class="row"><input type="checkbox" data-layer="${k}" ${v[k] ? "checked" : ""}>${color ? `<span class="sw" style="background:${color}"></span>` : ""}${label}</label>`;
    return `<h3>Sky picture</h3><select id="surveySel" aria-label="Sky picture">${SURVEYS.map((s) => `<option value="${esc(s.id)}" ${s.id === state.survey ? "selected" : ""}>${esc(s.label)}</option>`).join("")}</select>
      <p class="muted" id="surveyBand">${esc(SURVEYS.find((s) => s.id === state.survey)?.band || "")}</p>
      <h3>Drawn on top</h3>${row("constellations", "Constellation lines", "#5d7bd6")}${row("conNames", "Constellation names", "#8fa6ff")}${row("stars", "Bright star names", "#ffe9a8")}
      ${row("messier", "Messier galaxies, nebulae and clusters", "#4cc3ff")}${row("planets", "Sun, Moon and planets (now)", "#ff6ec7")}
      ${row("aegis", "AEGIS flagged stars", "#ff3d8b")}${row("coverage", "AEGIS survey coverage", "#2f8bff")}
      ${discRows()}
      <h3>View</h3><p><button class="btn ghost" data-proj="AIT">Whole-sky map</button><button class="btn ghost" data-proj="SIN">Globe</button><button class="btn ghost" data-proj="TAN">Flat (zoomed)</button></p>
      <p class="muted">The buttons on the sky itself add a coordinate grid, a SIMBAD pointer and full screen.</p>`;
  },
  tonight() {
    const loc = state.location, when = state.when || new Date();
    const local = new Date(when.getTime() - when.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
    const rows = bodyPositions(when).map((p) => `<tr><td><a href="#" data-goto="${p.ra},${p.dec}">${p.name}</a></td><td>${loc ? (p.alt > 0 ? `<span class="up">up ${p.alt.toFixed(0)}°</span>` : `<span class="down">down</span>`) : "–"}</td>
      <td>${loc && p.rise ? p.rise.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : "–"}</td><td>${loc && p.set ? p.set.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : "–"}</td></tr>`).join("");
    let moon = ""; try { const AE = window.Astronomy, t = AE.MakeTime(when); const f = AE.Illumination("Moon", t).phase_fraction; moon = `<p>Moon: ${(f * 100).toFixed(0)}% lit.</p>`; } catch {}
    try {
      if (loc && window.SkyDark) {
        const w = window.SkyDark.darkWindow(window.Astronomy, when, loc.lat, loc.lon), hm = (d) => d ? d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : "–";
        const hrs = (m) => `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, "0")} min`;
        const dark = w.dusk && w.dawn ? `Fully dark ${hm(w.dusk)} – ${hm(w.dawn)} (${hrs(w.darkMin)}); with the Moon down: <b>${hrs(w.moonFreeMin)}</b>.`
          : "The Sun never gets 18° below the horizon tonight, so the sky never gets fully dark.";
        moon = `<div class="darkwin" id="darkWin"><button class="btn ghost" id="printPlan" style="float:right">🖨 Print night plan</button><p><b>Dark sky tonight</b> · ${w.phase}, ${(w.lit * 100).toFixed(0)}% lit</p>
          <p>Sunset ${hm(w.sunset)} · Sunrise ${hm(w.sunrise)}</p><p>${dark}</p>
          <p class="muted">Faint galaxies and nebulae are best when it is fully dark and the Moon is down.</p></div>`;
        const best = state.data.messier ? window.SkyDark.bestTargets(window.Astronomy, state.data.messier.objects, loc.lat, loc.lon, w, 30, 10) : [];
        if (best.length) moon += `<h3>Best targets tonight</h3><table id="bestTargets"><tr><th>Object</th><th>Mag</th><th>Highest</th></tr>${best.map((o) =>
          `<tr><td><a href="#" data-goto="${o.ra},${o.dec}">${esc(o.id)}${o.common ? " · " + esc(o.common) : ""}</a></td><td>${o.mag}</td><td>${o.alt.toFixed(0)}° at ${hm(o.at)}</td></tr>`).join("")}</table>
          <p class="muted">Messier objects that climb above 30° while it is fully dark, brightest first. Tap one to go there.</p>`;
        moon = `<div id="nightPlan"><h2 class="printonly">Night plan · ${when.toLocaleDateString()} · ${loc.lat.toFixed(2)}°, ${loc.lon.toFixed(2)}°</h2>${moon}</div>`;
      }
    } catch {}
    return `<p>Where are the Sun, Moon and planets? ${loc ? "" : "Set your location to see what is above the horizon."}</p>
      <p><button class="btn" id="geo">Use my location</button></p>
      <p><label>Latitude <input type="number" id="lat" step="0.01" min="-90" max="90" value="${loc?.lat ?? ""}" style="width:7em"></label>
      <label>Longitude <input type="number" id="lon" step="0.01" min="-180" max="180" value="${loc?.lon ?? ""}" style="width:7em"></label> <button class="btn ghost" id="setLoc">Set</button></p>
      <p><label>Date and time <input type="datetime-local" id="when" value="${local}"></label> <button class="btn ghost" id="now">Now</button></p>
      ${moon}<table><tr><th>Body</th><th>Now</th><th>Next rise</th><th>Next set</th></tr>${rows}</table>
      <p class="muted">Your location stays on this device. Positions from astronomy-engine (accurate to about an arcminute).</p>`;
  },
  tour() {
    const s = TOUR[state.tourStep];
    return `<p class="muted">Step ${state.tourStep + 1} of ${TOUR.length}</p><h3>${esc(s.title)}</h3><p class="step">${esc(s.text)}</p>
      <div class="stepnav"><button class="btn ghost" id="prev" ${state.tourStep ? "" : "disabled"}>‹ Back</button><button class="btn" id="go">Show me</button><button class="btn ghost" id="next" ${state.tourStep < TOUR.length - 1 ? "" : "disabled"}>Next ›</button></div>`;
  },
  learn() {
    return `<h3>Lessons</h3>${LESSONS.map((l) => `<details class="lesson"><summary>${esc(l.title)}</summary>${l.body}</details>`).join("")}
      <h3>Classroom activities</h3>${ACTIVITIES.map((a) => `<details class="lesson"><summary>${esc(a.title)}</summary><p>${esc(a.body)}</p></details>`).join("")}
      <p class="muted">Tip for projectors: press <b>A+</b> for larger text, and use full screen from the sky's own buttons.</p>`;
  },
  aegis() {
    const F = state.data.flags, C = state.data.coverage, n = Object.keys(state.reviews).length;
    const cov = C && C.tiles_done ? `<p>Survey coverage: <b>${C.tiles_done.toLocaleString()}</b> of ${C.tiles_total.toLocaleString()} sky tiles, <b>${C.stars.toLocaleString()}</b> Gaia stars (generated ${esc(C.generated)}).</p>` : "";
    const legend = Object.entries(FLAG_COLORS).map(([k, c]) => `<div class="row"><span class="sw" style="background:${c}"></span><b>${esc(F?.criteria?.[k]?.label || FLAG_LABELS[k])}</b>${F?.counts_in_sweep?.[k] != null ? ` <span class="muted">(${F.counts_in_sweep[k].toLocaleString()} in the survey)</span>` : ""}</div>`).join("");
    const body = F && F.stars && F.stars.length
      ? `<p><b>${F.shown.toLocaleString()}</b> flagged stars are shown (${esc(F.selection)}). They are <b>${esc(F.status)}</b>.</p>${legend}<p>Click a cross on the sky, read why it was flagged, decide what would convince you, then vote.</p>`
      : `<p>The flagged-star layer is empty in this copy. On the computer that runs the AEGIS Star Mapper, run <code>tools/export_from_sweep.py</code> (see INSTALL.md) to add it, or load an exported <code>aegis_flags.json</code> here:</p><p><input type="file" id="loadFlags" accept="application/json,.json"></p>${legend}`;
    const DS = state.data.disc;
    const disc = DS && DS.counts && DS.rows_read ? `<h3>Discovery categories</h3><p>From ${DS.rows_read.toLocaleString()} stars (rules fixed in advance, PREREG_D716). Up to ${DS.top_n.toLocaleString()} of each are on the map; open Layers to show or hide them.</p><table>${Object.entries(DS.categories).map(([k, m]) => `<tr><td><span class="sw" style="background:${m.color};display:inline-block;width:.8em;height:.8em;border-radius:50%"></span> ${esc(m.label)}</td><td>${(DS.counts[k] ?? 0).toLocaleString()}</td></tr>`).join("")}</table>` : "";
    return `<p>The AEGIS Star Mapper swept the ESA Gaia DR3 catalogue tile by tile and re-checked every one of its 12,288 sky tiles against ESA's own counts: <b>192,208,838 stars, 0 mismatches</b> (audit completed 29 Oct 2026). It flags stars that look unusual so people can check them.</p>
      ${cov}${body}${disc}<h3>Your reviews</h3><p>${n} reviewed on this device. <button class="btn ghost" id="exportReviews" ${n ? "" : "disabled"}>Download CSV</button> <button class="btn ghost" id="clearReviews" ${n ? "" : "disabled"}>Clear</button></p>
      <p class="muted">Reviews never leave this device unless you download and share the file. No accounts, no tracking.</p>`;
  },
  about() {
    return `<p>A free sky map for classrooms and curious people, from the AEGIS project (Danny Lee Eldridge, Oklahoma City), built with AI assistance (Claude, Anthropic).</p>
      <h3>Credits</h3><ul><li>Sky viewer: <a href="https://aladin.cds.unistra.fr/AladinLite/" target="_blank" rel="noopener">Aladin Lite</a> by CDS, Strasbourg (LGPL-3).</li>
      <li>Sky images (HiPS) served by CDS: DSS, 2MASS, WISE, Mellinger, Planck, Fermi, VTSS and others; each survey's credits are in Aladin's layer menu.</li>
      <li>Gaia data: ESA mission <i>Gaia</i>, processed by the Gaia DPAC.</li>
      <li>Planets: <a href="https://github.com/cosinekitty/astronomy" target="_blank" rel="noopener">astronomy-engine</a> by Don Cross (MIT).</li>
      <li>Constellations, star names and Messier list: <a href="https://github.com/ofrohn/d3-celestial" target="_blank" rel="noopener">d3-celestial</a> data by Olaf Frohn (BSD-3).</li></ul>
      <p>Licence: AGPL-3.0-or-later (free for schools and everyone); see LICENSE and THIRD_PARTY_NOTICES.md.</p>
      <p><button class="btn ghost" id="theme">Switch light/dark</button></p>`;
  },
};
const TITLES = { layers: "Layers", tonight: "Tonight's sky", tour: "Guided tour", learn: "Learn", aegis: "AEGIS stars", about: "About" };

function openPanel(name) {
  const same = !$("#panel").hidden && state.panel === name;
  for (const b of document.querySelectorAll(".tabs button")) b.setAttribute("aria-expanded", String(!same && b.dataset.tab === name));
  if (same) { $("#panel").hidden = true; state.panel = null; return; }
  state.panel = name; $("#panelTitle").textContent = TITLES[name]; $("#panelBody").innerHTML = PANELS[name](); $("#panel").hidden = false; wirePanel(name);
}
function rerender() { if (state.panel) { $("#panelBody").innerHTML = PANELS[state.panel](); wirePanel(state.panel); } }

function wirePanel(name) {
  const B = $("#panelBody");
  for (const a of B.querySelectorAll("[data-goto]")) a.onclick = (e) => { e.preventDefault(); const [ra, dec] = a.dataset.goto.split(",").map(Number); goto(ra, dec, 20); };
  if (name === "layers") {
    $("#surveySel").onchange = (e) => { setSurvey(e.target.value); $("#surveyBand").textContent = SURVEYS.find((s) => s.id === e.target.value)?.band || ""; };
    for (const cb of B.querySelectorAll("[data-layer]")) cb.onchange = () => { state.visible[cb.dataset.layer] = cb.checked; applyVisibility(); };
    for (const cb of B.querySelectorAll("[data-disc]")) cb.onchange = () => { state.visible["disc_" + cb.dataset.disc] = cb.checked; applyVisibility(); };
    for (const p of B.querySelectorAll("[data-proj]")) p.onclick = () => { try { state.aladin.setProjection(p.dataset.proj); if (p.dataset.proj !== "TAN") state.aladin.setFoV(p.dataset.proj === "AIT" ? 220 : 120); } catch (e) { console.warn(e); } };
  }
  if (name === "tonight") {
    const pp = $("#printPlan"); if (pp) pp.onclick = () => { document.body.classList.add("printplan"); try { window.print(); } finally { setTimeout(() => document.body.classList.remove("printplan"), 500); } };
    $("#geo").onclick = () => navigator.geolocation?.getCurrentPosition((p) => { state.location = { lat: +p.coords.latitude.toFixed(2), lon: +p.coords.longitude.toFixed(2) }; store.set("location", state.location); updatePlanetLayer(); rerender(); }, () => alertNote("Location was not shared. You can type it in instead."));
    $("#setLoc").onclick = () => { const lat = parseFloat($("#lat").value), lon = parseFloat($("#lon").value); if (Math.abs(lat) <= 90 && Math.abs(lon) <= 180) { state.location = { lat, lon }; store.set("location", state.location); updatePlanetLayer(); rerender(); } };
    $("#when").onchange = (e) => { const d = new Date(e.target.value); if (!isNaN(d)) { state.when = d; updatePlanetLayer(); rerender(); } };
    $("#now").onclick = () => { state.when = null; updatePlanetLayer(); rerender(); };
  }
  if (name === "tour") {
    $("#prev").onclick = () => { state.tourStep = Math.max(0, state.tourStep - 1); rerender(); runStep(); };
    $("#next").onclick = () => { state.tourStep = Math.min(TOUR.length - 1, state.tourStep + 1); rerender(); runStep(); };
    $("#go").onclick = runStep;
  }
  if (name === "aegis") {
    const lf = $("#loadFlags"); if (lf) lf.onchange = async () => { try { const d = JSON.parse(await lf.files[0].text()); if (!Array.isArray(d.stars)) throw 0; state.data.flags = d; addFlagLayers(d); state.visible.aegis = true; applyVisibility(); rerender(); } catch { alertNote("That file is not an AEGIS flags export."); } };
    const ex = $("#exportReviews"); if (ex) ex.onclick = exportReviews;
    const cl = $("#clearReviews"); if (cl) cl.onclick = () => { if (confirmClear()) { state.reviews = {}; store.set("reviews", {}); rerender(); } };
  }
  if (name === "about") $("#theme").onclick = () => { const r = document.documentElement; const dark = r.dataset.theme !== "light" && !(r.dataset.theme === undefined && matchMedia("(prefers-color-scheme: light)").matches); r.dataset.theme = dark ? "light" : "dark"; store.set("theme", r.dataset.theme); };
}
function confirmClear() { return window.confirm("Clear all reviews saved on this device?"); }
function runStep() { const s = TOUR[state.tourStep]; if (s.survey) setSurvey(s.survey); if (s.layers) { for (const l of s.layers) state.visible[l] = true; applyVisibility(); } try { state.aladin.setProjection(s.fov > 100 ? "AIT" : "SIN"); } catch {} goto(s.ra, s.dec, s.fov); }
function exportReviews() {
  const rows = [["source_id", "vote", "flags", "ra", "dec", "time_utc"]].concat(Object.entries(state.reviews).map(([id, r]) => [id, r.vote, r.flags, r.ra, r.dec, r.t]));
  const csv = rows.map((r) => r.map((x) => `"${String(x ?? "").replace(/"/g, '""')}"`).join(",")).join("\n");
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" })); a.download = "aegis_reviews.csv"; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
}
function alertNote(msg) { const n = $("#netNote"); n.textContent = msg; n.hidden = false; setTimeout(() => (n.hidden = true), 6000); }

// ---------- search ----------
function buildSearch() {
  const idx = [], D = state.data;
  for (const c of D.cons?.constellations || []) idx.push({ key: c.name, alt: [c.latin, c.id], ra: c.label[0], dec: c.label[1], fov: 30, d: { kind: "constellation", ...c, lines: undefined } });
  for (const s of D.stars?.stars || []) idx.push({ key: s.name, alt: [s.desig], ra: s.ra, dec: s.dec, fov: 2, d: { kind: "star", label: s.name, ...s } });
  for (const m of D.messier?.objects || []) idx.push({ key: m.id + (m.common ? " " + m.common : ""), alt: [m.id, m.ngc, m.common], ra: m.ra, dec: m.dec, fov: 1, d: { kind: "messier", ...m } });
  for (const b of BODIES) idx.push({ key: b, alt: [], planet: b });
  state.index = idx;
  $("#searchList").innerHTML = idx.map((i) => `<option value="${esc(i.key)}">`).join("");
  $("#searchForm").onsubmit = (e) => {
    e.preventDefault(); const q = $("#search").value.trim().toLowerCase(); if (!q) return;
    const hit = idx.find((i) => i.key.toLowerCase() === q || i.alt.some((a) => a && a.toLowerCase() === q)) || idx.find((i) => i.key.toLowerCase().startsWith(q));
    if (hit?.planet) { const p = bodyPositions(state.when || new Date()).find((x) => x.name === hit.planet); goto(p.ra, p.dec, 3); showInfo({ kind: "planet", label: p.name, ...p, when: (state.when || new Date()).toISOString() }); return; }
    if (hit) { goto(hit.ra, hit.dec, hit.fov); showInfo(hit.d); return; }
    const gid = q.replace(/^gaia\s*dr3\s*/, "");
    if (/^\d{6,}$/.test(gid)) {
      let st = null;
      for (const x of D.flags?.stars || []) if (x.id === gid) st = { ...x };
      for (const [k, l] of Object.entries(D.disc?.stars || {})) for (const x of l) if (x.id === gid) st = { ...x, ...(st || {}), cats: [...(st?.cats || []), k] };
      if (st) { goto(st.ra, st.dec, 0.05); showInfo({ kind: "aegis", ...st }); return; }
    }
    if (!navigator.onLine) { alertNote("Not in the built-in list, and the name lookup needs the internet. Try a constellation, a bright star, a Messier number or a planet."); return; }
    let answered = false; const miss = () => { if (!answered) { answered = true; alertNote("Not found. Try a constellation, a bright star, a Messier number or a planet."); } };
    setTimeout(miss, 6000);
    try { state.aladin.gotoObject($("#search").value.trim(), { success: () => { answered = true; }, error: miss }); } catch { miss(); }
  };
}

// ---------- start ----------
async function main() {
  const theme = store.get("theme", null); if (theme) document.documentElement.dataset.theme = theme;
  const big = store.get("big", false); document.documentElement.classList.toggle("big", big); $("#bigText").setAttribute("aria-pressed", String(big));
  $("#bigText").onclick = () => { const on = !document.documentElement.classList.contains("big"); document.documentElement.classList.toggle("big", on); $("#bigText").setAttribute("aria-pressed", String(on)); store.set("big", on); };
  for (const b of document.querySelectorAll(".tabs button")) b.onclick = () => openPanel(b.dataset.tab);
  $("#closePanel").onclick = () => openPanel(state.panel);
  $("#closeInfo").onclick = () => ($("#info").hidden = true);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { $("#info").hidden = true; if (state.panel) openPanel(state.panel); } });
  const [cons, stars, messier, flags, coverage, disc, reviewsAll] = await Promise.all(["constellations", "stars", "messier", "aegis_flags", "aegis_coverage", "aegis_discoveries", "aegis_reviews"].map((f) => loadJSON(`data/${f}.json`)));
  Object.assign(state.data, { cons, stars, messier, flags, coverage, disc, reviewsAll });
  buildSearch();
  window.__skymap = state;
  if (await initSky()) { try { buildLayers(); } catch (e) { console.error("layers", e); } setInterval(() => { if (!state.when) updatePlanetLayer(); }, 60000); }
  if (!navigator.onLine) alertNote("You are offline: telescope images need the internet. Drawn layers, Tonight, Tour and Learn still work.");
  else fetch("https://alasky.cds.unistra.fr/MocServer/query?ID=CDS/P/DSS2/color&get=id", { mode: "no-cors", cache: "no-store" }).catch(() => alertNote("The telescope image server (CDS) cannot be reached from this network, so only the drawn layers are shown."));
  if ("serviceWorker" in navigator && location.protocol !== "file:" && location.hostname !== "appassets.androidplatform.net") navigator.serviceWorker.register("sw.js").catch(() => {});
  window.__skymap = state; // for tests and the curious
}
main();
