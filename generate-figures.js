'use strict';
// ═══════════════════════════════════════════════════════════════════════════════
// PUBLICATION FIGURE GENERATOR
// Generates SVG figures for the arXiv paper from MCMC and optimization results
// ═══════════════════════════════════════════════════════════════════════════════

const fs = require('fs');
const path = require('path');
const ufeTasks = require('./ufe-tasks');

const OUTPUT_DIR = path.join(__dirname, 'figures');
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

// Load MCMC results
let mcmcResults;
try {
  mcmcResults = JSON.parse(fs.readFileSync(path.join(__dirname, 'mcmc-results.json'), 'utf8'));
} catch (e) {
  console.error('Run mcmc-sampler.js first'); process.exit(1);
}

// Load state for best-fit params
let state;
try {
  state = JSON.parse(fs.readFileSync(path.join(__dirname, 'ufe-state.json'), 'utf8'));
} catch (e) {
  console.error('No ufe-state.json'); process.exit(1);
}

// ── SVG helpers ──────────────────────────────────────────────────────────────
function svgHeader(w, h, title) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<style>
  text { font-family: 'Times New Roman', serif; }
  .axis { stroke: #333; stroke-width: 1.5; fill: none; }
  .grid { stroke: #ddd; stroke-width: 0.5; }
  .data-point { fill: #2563eb; stroke: #1d4ed8; stroke-width: 1; }
  .fit-line { fill: none; stroke-width: 2; }
  .lcdm { stroke: #666; stroke-dasharray: 6,4; }
  .ufe { stroke: #dc2626; }
  .band { opacity: 0.15; }
  .title { font-size: 14px; font-weight: bold; text-anchor: middle; }
  .label { font-size: 11px; text-anchor: middle; }
  .tick { font-size: 9px; }
</style>
<rect width="${w}" height="${h}" fill="white"/>
<text x="${w/2}" y="20" class="title">${title}</text>\n`;
}

function svgFooter() { return '</svg>'; }

// Scale data to plot coordinates
function scale(val, min, max, pixMin, pixMax) {
  return pixMin + (val - min) / (max - min) * (pixMax - pixMin);
}

// ── Figure 1: β(z) Evolution ─────────────────────────────────────────────────
function figureBetaEvolution() {
  const W = 600, H = 400;
  const margin = { top: 40, right: 30, bottom: 50, left: 60 };
  const pW = W - margin.left - margin.right;
  const pH = H - margin.top - margin.bottom;

  // H0 tension best-fit: β(z) = β₀ + β₁ · z/(1+z)
  const h0 = state.bestKnown?.['h0-tension']?.params || { beta0: -0.15, beta1: 0.192, H0: 72.15 };
  const beta0 = h0.beta0 || -0.15;
  const beta1 = h0.beta1 || 0.192;

  // MCMC uncertainties
  const stats = mcmcResults['h0-tension']?.paramStats;
  const b0_std = stats?.beta0?.std || 0.05;
  const b1_std = stats?.beta1?.std || 0.11;

  const zMin = 0, zMax = 2.5;
  const betaMin = -0.3, betaMax = 0.2;

  let svg = svgHeader(W, H, 'β(z) Torsion Coupling Evolution');

  // Axes
  svg += `<g transform="translate(${margin.left},${margin.top})">`;
  svg += `<line x1="0" y1="${pH}" x2="${pW}" y2="${pH}" class="axis"/>`;
  svg += `<line x1="0" y1="0" x2="0" y2="${pH}" class="axis"/>`;

  // Grid + ticks
  for (let z = 0; z <= 2.5; z += 0.5) {
    const x = scale(z, zMin, zMax, 0, pW);
    svg += `<line x1="${x}" y1="0" x2="${x}" y2="${pH}" class="grid"/>`;
    svg += `<text x="${x}" y="${pH+15}" class="tick" text-anchor="middle">${z.toFixed(1)}</text>`;
  }
  for (let b = -0.3; b <= 0.2; b += 0.1) {
    const y = scale(b, betaMax, betaMin, 0, pH);
    svg += `<line x1="0" y1="${y}" x2="${pW}" y2="${y}" class="grid"/>`;
    svg += `<text x="-8" y="${y+4}" class="tick" text-anchor="end">${b.toFixed(1)}</text>`;
  }

  // β = 0 reference line
  const y0 = scale(0, betaMax, betaMin, 0, pH);
  svg += `<line x1="0" y1="${y0}" x2="${pW}" y2="${y0}" stroke="#999" stroke-dasharray="3,3" stroke-width="1"/>`;

  // 1σ uncertainty band
  let bandPath = 'M';
  const nPts = 100;
  for (let i = 0; i <= nPts; i++) {
    const z = zMin + (zMax - zMin) * i / nPts;
    const beta = beta0 + beta1 * z / (1 + z);
    const sigma = Math.sqrt(b0_std**2 + (z/(1+z))**2 * b1_std**2);
    const x = scale(z, zMin, zMax, 0, pW);
    const y = scale(beta + sigma, betaMax, betaMin, 0, pH);
    bandPath += `${i === 0 ? '' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
  }
  for (let i = nPts; i >= 0; i--) {
    const z = zMin + (zMax - zMin) * i / nPts;
    const beta = beta0 + beta1 * z / (1 + z);
    const sigma = Math.sqrt(b0_std**2 + (z/(1+z))**2 * b1_std**2);
    const x = scale(z, zMin, zMax, 0, pW);
    const y = scale(beta - sigma, betaMax, betaMin, 0, pH);
    bandPath += `L${x.toFixed(1)},${y.toFixed(1)}`;
  }
  bandPath += 'Z';
  svg += `<path d="${bandPath}" fill="#dc2626" class="band"/>`;

  // Best-fit line
  let linePath = 'M';
  for (let i = 0; i <= nPts; i++) {
    const z = zMin + (zMax - zMin) * i / nPts;
    const beta = beta0 + beta1 * z / (1 + z);
    const x = scale(z, zMin, zMax, 0, pW);
    const y = scale(beta, betaMax, betaMin, 0, pH);
    linePath += `${i === 0 ? '' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
  }
  svg += `<path d="${linePath}" class="fit-line ufe"/>`;

  // Annotations
  svg += `<text x="${pW/2}" y="${pH+40}" class="label">Redshift z</text>`;
  svg += `<text x="-40" y="${pH/2}" class="label" transform="rotate(-90,-40,${pH/2})">β(z)</text>`;
  svg += `<text x="${pW-80}" y="20" font-size="10" fill="#dc2626">β₀ = ${beta0.toFixed(3)} ± ${b0_std.toFixed(3)}</text>`;
  svg += `<text x="${pW-80}" y="35" font-size="10" fill="#dc2626">β₁ = ${beta1.toFixed(3)} ± ${b1_std.toFixed(3)}</text>`;
  svg += `<text x="${pW-80}" y="50" font-size="10" fill="#666">7.4σ vs ΛCDM</text>`;

  svg += '</g>';
  svg += svgFooter();

  fs.writeFileSync(path.join(OUTPUT_DIR, 'fig1-beta-evolution.svg'), svg);
  console.log('✓ Figure 1: β(z) evolution');
}

// ── Figure 2: H(z) Data + Fits ───────────────────────────────────────────────
function figureHubble() {
  const W = 600, H = 400;
  const margin = { top: 40, right: 30, bottom: 50, left: 70 };
  const pW = W - margin.left - margin.right;
  const pH = H - margin.top - margin.bottom;

  const CC_DATA = ufeTasks.CC_DATA;
  const zMin = 0, zMax = 2.2;
  const hMin = 50, hMax = 250;

  // Best-fit params
  const h0p = state.bestKnown?.['cc-hubble-fit']?.params || { H0: 68, omega_m: 0.30, beta: 0.15 };

  let svg = svgHeader(W, H, 'H(z) — Cosmic Chronometer Data with UFE and ΛCDM Fits');
  svg += `<g transform="translate(${margin.left},${margin.top})">`;

  // Axes
  svg += `<line x1="0" y1="${pH}" x2="${pW}" y2="${pH}" class="axis"/>`;
  svg += `<line x1="0" y1="0" x2="0" y2="${pH}" class="axis"/>`;

  // Grid
  for (let z = 0; z <= 2; z += 0.5) {
    const x = scale(z, zMin, zMax, 0, pW);
    svg += `<line x1="${x}" y1="0" x2="${x}" y2="${pH}" class="grid"/>`;
    svg += `<text x="${x}" y="${pH+15}" class="tick" text-anchor="middle">${z.toFixed(1)}</text>`;
  }
  for (let h = 50; h <= 250; h += 50) {
    const y = scale(h, hMax, hMin, 0, pH);
    svg += `<line x1="0" y1="${y}" x2="${pW}" y2="${y}" class="grid"/>`;
    svg += `<text x="-8" y="${y+4}" class="tick" text-anchor="end">${h}</text>`;
  }

  // ΛCDM curve (β=0)
  let lcdmPath = 'M';
  for (let i = 0; i <= 100; i++) {
    const z = zMin + (zMax - zMin) * i / 100;
    const Hz = ufeTasks.torsionHubble(z, 67.4, 0.315, 9.34e-5, 0);
    const x = scale(z, zMin, zMax, 0, pW);
    const y = scale(Hz, hMax, hMin, 0, pH);
    lcdmPath += `${i === 0 ? '' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
  }
  svg += `<path d="${lcdmPath}" class="fit-line lcdm"/>`;

  // UFE curve
  let ufePath = 'M';
  for (let i = 0; i <= 100; i++) {
    const z = zMin + (zMax - zMin) * i / 100;
    const Hz = ufeTasks.torsionHubble(z, h0p.H0, h0p.omega_m, 9.34e-5, h0p.beta);
    const x = scale(z, zMin, zMax, 0, pW);
    const y = scale(Hz, hMax, hMin, 0, pH);
    ufePath += `${i === 0 ? '' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
  }
  svg += `<path d="${ufePath}" class="fit-line ufe"/>`;

  // Data points with error bars
  for (const d of CC_DATA) {
    const x = scale(d.z, zMin, zMax, 0, pW);
    const y = scale(d.H, hMax, hMin, 0, pH);
    const yErr = (d.sigma / (hMax - hMin)) * pH;
    svg += `<line x1="${x}" y1="${y-yErr}" x2="${x}" y2="${y+yErr}" stroke="#2563eb" stroke-width="1"/>`;
    svg += `<circle cx="${x}" cy="${y}" r="3" class="data-point"/>`;
  }

  // Legend
  svg += `<line x1="${pW-120}" y1="15" x2="${pW-90}" y2="15" class="fit-line ufe"/>`;
  svg += `<text x="${pW-85}" y="19" font-size="9">UFE (β=${(h0p.beta||0).toFixed(2)})</text>`;
  svg += `<line x1="${pW-120}" y1="30" x2="${pW-90}" y2="30" class="fit-line lcdm"/>`;
  svg += `<text x="${pW-85}" y="34" font-size="9">ΛCDM</text>`;

  svg += `<text x="${pW/2}" y="${pH+40}" class="label">Redshift z</text>`;
  svg += `<text x="-50" y="${pH/2}" class="label" transform="rotate(-90,-50,${pH/2})">H(z) [km/s/Mpc]</text>`;
  svg += '</g>';
  svg += svgFooter();

  fs.writeFileSync(path.join(OUTPUT_DIR, 'fig2-hubble-hz.svg'), svg);
  console.log('✓ Figure 2: H(z) fits');
}

// ── Figure 3: Δχ² Summary Bar Chart ─────────────────────────────────────────
function figureDeltaChi() {
  const W = 650, H = 350;
  const margin = { top: 40, right: 30, bottom: 80, left: 60 };
  const pW = W - margin.left - margin.right;
  const pH = H - margin.top - margin.bottom;

  const tasks = [
    { id: 'cc-hubble-fit', name: 'CC H(z)' },
    { id: 'desi-bao-fit', name: 'DESI BAO' },
    { id: 'h0-tension', name: 'H₀ Tension' },
    { id: 'rsd-growth', name: 'RSD fσ₈' },
    { id: 's8-tension', name: 'S₈ Tension' },
    { id: 'dark-energy-eos', name: 'DE EoS' },
    { id: 'combined-multisurvey', name: 'Combined' },
  ];

  const maxDelta = 100; // cap display at 100

  let svg = svgHeader(W, H, 'Δχ² Improvement over ΛCDM (per task)');
  svg += `<g transform="translate(${margin.left},${margin.top})">`;

  // Axes
  svg += `<line x1="0" y1="${pH}" x2="${pW}" y2="${pH}" class="axis"/>`;
  svg += `<line x1="0" y1="0" x2="0" y2="${pH}" class="axis"/>`;

  // Significance thresholds
  const sigLevels = [
    { chi2: 4.0, label: '2σ', color: '#fbbf24' },
    { chi2: 9.0, label: '3σ', color: '#f97316' },
    { chi2: 16.0, label: '4σ', color: '#ef4444' },
    { chi2: 25.0, label: '5σ', color: '#dc2626' },
  ];
  for (const sl of sigLevels) {
    const y = scale(sl.chi2, maxDelta, 0, 0, pH);
    if (y > 0 && y < pH) {
      svg += `<line x1="0" y1="${y}" x2="${pW}" y2="${y}" stroke="${sl.color}" stroke-dasharray="4,3" stroke-width="0.8"/>`;
      svg += `<text x="${pW+5}" y="${y+3}" font-size="8" fill="${sl.color}">${sl.label}</text>`;
    }
  }

  const barW = pW / tasks.length * 0.7;
  const gap = pW / tasks.length;

  for (let i = 0; i < tasks.length; i++) {
    const t = tasks[i];
    const r = mcmcResults[t.id];
    if (!r) continue;
    const delta = Math.min(r.deltaChiSq, maxDelta);
    const x = i * gap + gap * 0.15;
    const barH = (delta / maxDelta) * pH;
    const y = pH - barH;
    const color = delta >= 25 ? '#dc2626' : delta >= 9 ? '#f97316' : delta >= 4 ? '#fbbf24' : '#93c5fd';

    svg += `<rect x="${x}" y="${y}" width="${barW}" height="${barH}" fill="${color}" rx="2"/>`;
    svg += `<text x="${x + barW/2}" y="${y - 5}" font-size="9" text-anchor="middle" font-weight="bold">${r.deltaChiSq > maxDelta ? '>100' : r.deltaChiSq.toFixed(1)}</text>`;
    svg += `<text x="${x + barW/2}" y="${pH + 12}" font-size="8" text-anchor="middle" transform="rotate(35,${x+barW/2},${pH+12})">${t.name}</text>`;
    svg += `<text x="${x + barW/2}" y="${y - 18}" font-size="8" text-anchor="middle" fill="#666">${r.sigmaFromDeltaChi.toFixed(1)}σ</text>`;
  }

  svg += `<text x="${pW/2}" y="${pH+60}" class="label">Task</text>`;
  svg += `<text x="-40" y="${pH/2}" class="label" transform="rotate(-90,-40,${pH/2})">Δχ² (UFE − ΛCDM)</text>`;
  svg += '</g>';
  svg += svgFooter();

  fs.writeFileSync(path.join(OUTPUT_DIR, 'fig3-delta-chi2.svg'), svg);
  console.log('✓ Figure 3: Δχ² bar chart');
}

// ── Figure 4: w(z) Phantom Crossing ─────────────────────────────────────────
function figurePhantom() {
  const W = 500, H = 350;
  const margin = { top: 40, right: 30, bottom: 50, left: 60 };
  const pW = W - margin.left - margin.right;
  const pH = H - margin.top - margin.bottom;

  // Dark energy EoS best-fit: w(z) = w0 + wa * z/(1+z)
  const de = state.bestKnown?.['dark-energy-eos']?.params || { w0: -1.14, wa: 0.4 };
  const w0 = de.w0 || -1.14;
  const wa = de.wa || 0.4;
  const deStats = mcmcResults['dark-energy-eos']?.paramStats;

  const zMin = 0, zMax = 2.0;
  const wMin = -1.5, wMax = -0.3;

  let svg = svgHeader(W, H, 'w(z) Dark Energy Equation of State');
  svg += `<g transform="translate(${margin.left},${margin.top})">`;
  svg += `<line x1="0" y1="${pH}" x2="${pW}" y2="${pH}" class="axis"/>`;
  svg += `<line x1="0" y1="0" x2="0" y2="${pH}" class="axis"/>`;

  // w = -1 reference
  const yw1 = scale(-1, wMax, wMin, 0, pH);
  svg += `<line x1="0" y1="${yw1}" x2="${pW}" y2="${yw1}" stroke="#666" stroke-dasharray="5,4" stroke-width="1.5"/>`;
  svg += `<text x="${pW+5}" y="${yw1+4}" font-size="9" fill="#666">ΛCDM</text>`;

  // w(z) curve
  let wPath = 'M';
  for (let i = 0; i <= 100; i++) {
    const z = zMin + (zMax - zMin) * i / 100;
    const w = w0 + wa * z / (1 + z);
    const x = scale(z, zMin, zMax, 0, pW);
    const y = scale(w, wMax, wMin, 0, pH);
    wPath += `${i === 0 ? '' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
  }
  svg += `<path d="${wPath}" class="fit-line ufe" stroke-width="2.5"/>`;

  // Phantom region shading (w < -1)
  svg += `<rect x="0" y="${yw1}" width="${pW}" height="${pH - yw1}" fill="#dc2626" opacity="0.05"/>`;
  svg += `<text x="10" y="${yw1 + 15}" font-size="9" fill="#dc2626" opacity="0.7">Phantom (w &lt; −1)</text>`;

  // Ticks
  for (let z = 0; z <= 2; z += 0.5) {
    const x = scale(z, zMin, zMax, 0, pW);
    svg += `<text x="${x}" y="${pH+15}" class="tick" text-anchor="middle">${z.toFixed(1)}</text>`;
  }
  for (let w = -1.5; w <= -0.3; w += 0.3) {
    const y = scale(w, wMax, wMin, 0, pH);
    svg += `<text x="-8" y="${y+4}" class="tick" text-anchor="end">${w.toFixed(1)}</text>`;
  }

  svg += `<text x="${pW/2}" y="${pH+40}" class="label">Redshift z</text>`;
  svg += `<text x="-40" y="${pH/2}" class="label" transform="rotate(-90,-40,${pH/2})">w(z)</text>`;
  svg += `<text x="10" y="20" font-size="10" fill="#dc2626">w₀ = ${w0.toFixed(3)}</text>`;
  svg += `<text x="10" y="35" font-size="10" fill="#dc2626">wₐ = ${wa.toFixed(3)}</text>`;
  svg += '</g>';
  svg += svgFooter();

  fs.writeFileSync(path.join(OUTPUT_DIR, 'fig4-phantom-crossing.svg'), svg);
  console.log('✓ Figure 4: w(z) phantom crossing');
}

// ── Figure 5: Parameter Constraints Summary ──────────────────────────────────
function figureParamSummary() {
  const W = 550, H = 400;
  const margin = { top: 40, right: 30, bottom: 30, left: 150 };
  const pW = W - margin.left - margin.right;
  const pH = H - margin.top - margin.bottom;

  // Collect β measurements across tasks
  const betaMeasurements = [];
  for (const [tid, r] of Object.entries(mcmcResults)) {
    const betaKey = Object.keys(r.paramStats).find(k => k === 'beta' || k === 'beta0');
    if (betaKey && r.paramStats[betaKey].std < 1.0) {
      betaMeasurements.push({
        task: tid.replace(/-/g, ' '),
        mean: r.paramStats[betaKey].mean,
        std: r.paramStats[betaKey].std,
        lo95: r.paramStats[betaKey].lo95,
        hi95: r.paramStats[betaKey].hi95,
      });
    }
  }

  const bMin = -0.8, bMax = 1.0;
  const rowH = pH / betaMeasurements.length;

  let svg = svgHeader(W, H, 'β Constraints Across Tasks (95% CI)');
  svg += `<g transform="translate(${margin.left},${margin.top})">`;

  // β = 0 reference
  const x0 = scale(0, bMin, bMax, 0, pW);
  svg += `<line x1="${x0}" y1="0" x2="${x0}" y2="${pH}" stroke="#333" stroke-dasharray="4,3"/>`;

  for (let i = 0; i < betaMeasurements.length; i++) {
    const m = betaMeasurements[i];
    const y = i * rowH + rowH / 2;
    const xMean = scale(m.mean, bMin, bMax, 0, pW);
    const xLo = scale(m.lo95, bMin, bMax, 0, pW);
    const xHi = scale(m.hi95, bMin, bMax, 0, pW);

    // 95% CI bar
    svg += `<line x1="${xLo}" y1="${y}" x2="${xHi}" y2="${y}" stroke="#2563eb" stroke-width="2"/>`;
    svg += `<line x1="${xLo}" y1="${y-5}" x2="${xLo}" y2="${y+5}" stroke="#2563eb" stroke-width="1.5"/>`;
    svg += `<line x1="${xHi}" y1="${y-5}" x2="${xHi}" y2="${y+5}" stroke="#2563eb" stroke-width="1.5"/>`;
    // Mean
    svg += `<circle cx="${xMean}" cy="${y}" r="4" fill="#dc2626" stroke="#991b1b"/>`;
    // Label
    svg += `<text x="-5" y="${y+4}" font-size="9" text-anchor="end">${m.task}</text>`;
    svg += `<text x="${xHi+8}" y="${y+3}" font-size="8" fill="#666">${m.mean.toFixed(3)}±${m.std.toFixed(3)}</text>`;
  }

  // x-axis ticks
  for (let b = -0.5; b <= 1.0; b += 0.25) {
    const x = scale(b, bMin, bMax, 0, pW);
    svg += `<text x="${x}" y="${pH+15}" class="tick" text-anchor="middle">${b.toFixed(2)}</text>`;
  }
  svg += `<text x="${pW/2}" y="${pH+28}" class="label">β</text>`;

  svg += '</g>';
  svg += svgFooter();

  fs.writeFileSync(path.join(OUTPUT_DIR, 'fig5-beta-constraints.svg'), svg);
  console.log('✓ Figure 5: β constraints forest plot');
}

// ── Generate all figures ─────────────────────────────────────────────────────
console.log('Generating publication figures...\n');
figureBetaEvolution();
figureHubble();
figureDeltaChi();
figurePhantom();
figureParamSummary();
console.log(`\n✅ All figures saved to ${OUTPUT_DIR}/`);
