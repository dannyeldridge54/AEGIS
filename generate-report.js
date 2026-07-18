/**
 * AEGIS / Seeker — Scientific Report Generator
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Generates a publication-quality technical report in the style of
 * Physical Review D / JCAP / Classical and Quantum Gravity.
 *
 * Pulls live optimization data from AEGIS and Seeker monitoring endpoints
 * and formats results with proper scientific structure.
 *
 * Usage:
 *   node generate-report.js                    → prints markdown to stdout
 *   node generate-report.js --out report.md    → writes markdown file
 *   node generate-report.js --out report.html --format html  → styled HTML
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

// ─── Fetch monitor data ──────────────────────────────────────────────────────

function fetchJSON(port, endpoint) {
  return new Promise((resolve, reject) => {
    const req = http.get(`http://localhost:${port}${endpoint}`, { timeout: 5000 }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { resolve(null); }
      });
    });
    req.on('error', () => resolve(null));
    req.on('timeout', () => { req.destroy(); resolve(null); });
  });
}

async function gatherData() {
  const [aegisSnap, seekerSnap, aegisAlerts, seekerAlerts] = await Promise.all([
    fetchJSON(5555, '/api/snapshot'),
    fetchJSON(5556, '/api/snapshot'),
    fetchJSON(5555, '/api/alerts'),
    fetchJSON(5556, '/api/alerts'),
  ]);
  return { aegisSnap, seekerSnap, aegisAlerts, seekerAlerts };
}

// ─── Report sections ─────────────────────────────────────────────────────────

function formatTimestamp(ts) {
  if (!ts) return 'N/A';
  return new Date(ts).toISOString().replace('T', ' ').replace(/\.\d+Z/, ' UTC');
}

function formatDuration(seconds) {
  if (!seconds || seconds < 0) return 'N/A';
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) return `${h}h ${m}m ${s}s`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}

function formatNumber(n, digits = 6) {
  if (n === null || n === undefined) return 'N/A';
  if (Math.abs(n) < 0.001 && n !== 0) return n.toExponential(digits);
  if (Math.abs(n) > 1e6) return n.toExponential(digits);
  return n.toPrecision(digits);
}

function classifyTorsionRun(runId) {
  if (runId.includes('einstein-cartan')) return 'Einstein-Cartan';
  if (runId.includes('ft-gravity')) return 'f(T) Gravity';
  if (runId.includes('ufe-torsion')) return 'UFE Torsion';
  if (runId.includes('torsion-wave')) return 'Torsion Wave';
  return null;
}

function extractTorsionRuns(snapshot) {
  if (!snapshot || !snapshot.runs) return [];
  return Object.values(snapshot.runs).filter(r => classifyTorsionRun(r.id));
}

function extractTorsionAlerts(alerts) {
  if (!alerts) return [];
  return alerts.filter(a => {
    const id = a.id || a.data?.runId || '';
    return id.includes('torsion') || id.includes('einstein') || id.includes('ft-gravity') || id.includes('ufe-torsion');
  });
}

function filterAnomalies(alerts) {
  if (!alerts) return [];
  return alerts.filter(a => a.category === 'anomaly' || a.severity === 'critical');
}

function filterBreakthroughs(alerts) {
  if (!alerts) return [];
  return alerts.filter(a => a.category === 'breakthrough' || a.severity === 'breakthrough');
}

function filterInsights(alerts) {
  if (!alerts) return [];
  return alerts.filter(a => a.category === 'insight');
}

// ─── Build Markdown report ───────────────────────────────────────────────────

function buildReport(data) {
  const { aegisSnap, seekerSnap, aegisAlerts, seekerAlerts } = data;
  const now = new Date();
  const allAlerts = [...(aegisAlerts || []), ...(seekerAlerts || [])];
  const anomalies = filterAnomalies(allAlerts);
  const breakthroughs = filterBreakthroughs(allAlerts);
  const insights = filterInsights(allAlerts);

  const aegisTorsionRuns = extractTorsionRuns(aegisSnap);
  const seekerTorsionRuns = extractTorsionRuns(seekerSnap);
  const allTorsionRuns = [...aegisTorsionRuns, ...seekerTorsionRuns];

  // Compute stats
  const aegisUptime = aegisSnap ? formatDuration(aegisSnap.uptime) : 'offline';
  const seekerUptime = seekerSnap ? formatDuration(seekerSnap.uptime) : 'offline';
  const totalEvals = (aegisSnap?.summary?.totalEvals || 0) + (seekerSnap?.summary?.totalEvals || 0);
  const totalRuns = (aegisSnap?.summary?.totalRuns || 0) + (seekerSnap?.summary?.totalRuns || 0);

  let report = '';

  // ── Header ──
  report += `# Torsion Field Theory — Computational Anomaly & Discovery Report

> **Principal Investigator:** Danny Lee Eldridge
> **Date:** ${now.toISOString().slice(0, 10)}
> **Report Generated:** ${now.toISOString().replace('T', ' ').slice(0, 19)} UTC
> **Engines:** AEGIS v1.0 + Seeker v1.0 (Dual Pincer Configuration)
> **Classification:** Preliminary Computational Results — Pre-Print

---

## Abstract

This report summarizes anomalies, breakthroughs, and key insights discovered by
the AEGIS/Seeker autonomous optimization framework while exploring spacetime
torsion parameter spaces. Two independent engines operate in a pincer strategy —
AEGIS sweeping from exploration toward exploitation while Seeker converges from
the opposite direction — ensuring comprehensive coverage of the torsion field
landscape.

Four torsion theory domains are under continuous investigation:

1. **Einstein-Cartan torsion** — 6-component spin-torsion coupling in Riemann-Cartan geometry
2. **Teleparallel f(T) gravity** — Modified gravity via torsion scalar with cosmological H(z) fitting
3. **UFE torsion functional** — Unified field-energy functional Φ(T, S, K) with physical constraints
4. **Torsion wave propagation** — Massive torsion field equation □T + m²T + λT³ = J

---

## 1. Computational Infrastructure

| Metric | Value |
|--------|-------|
| AEGIS uptime | ${aegisUptime} |
| Seeker uptime | ${seekerUptime} |
| Total function evaluations | ${totalEvals.toLocaleString()} |
| Total optimization runs | ${totalRuns} |
| Torsion-specific runs | ${allTorsionRuns.length} |
| Active anomaly alerts | ${anomalies.length} |
| Breakthrough events | ${breakthroughs.length} |
| Key insights | ${insights.length} |

**Methodology:** Both engines use adaptive meta-learning across 10 optimization
strategies (gradient descent, Bayesian surrogate, simulated annealing, particle
swarm, evolutionary, novelty search, multi-armed bandit, grid search, random
sampling, pure exploitation). Each run is seeded for reproducibility. UFE
(Useful Function Evaluation) tracking measures optimization efficiency.
Strategy selection adapts online based on observed improvement rates.

**Pincer Strategy:** AEGIS begins each cycle with exploration-heavy profiles
(high exploration rate, curiosity-driven strategies) paired with easy tasks, and
progresses toward exploitation-heavy profiles on harder tasks. Seeker does the
reverse. Each cycle they swap direction, guaranteeing complete coverage.

---

## 2. Torsion Parameter Spaces Under Investigation

### 2.1 Einstein-Cartan Torsion (8 parameters)

Explores the antisymmetric torsion tensor T^a_{bc} in 4D Riemann-Cartan spacetime.
The cost function minimizes the Cartan equation residual:

\`\`\`
Residual = |T^a_{bc} - 8πG · s^a_{bc}|² + λ · T_{scalar}² + trace penalties
\`\`\`

| Parameter | Range | Description |
|-----------|-------|-------------|
| T01, T02, T03, T12, T13, T23 | [-1, 1] | 6 independent torsion components |
| spinDensity | [0, 10²⁰] | Spin angular momentum density |
| couplingLambda | [-10, 10] | Torsion-curvature coupling strength |

### 2.2 f(T) Teleparallel Gravity (5 parameters)

Fits modified teleparallel gravity models to 21 observational H(z) data points
(Planck 2018 + BAO + cosmic chronometers, z = 0 to z = 2.34).

Four model types compete:
- **Power law:** f(T) = α·T^n
- **Born-Infeld:** f(T) = λ(√(1 + 2T/λ) − 1)
- **Logarithmic:** f(T) = α·T + β·T·ln(T/T₀)
- **Exponential:** f(T) = α·T(1 − e^{β·T₀/T})

Baseline: ΛCDM with H₀ = 67.4 km/s/Mpc, Ω_m = 0.315.

### 2.3 UFE Torsion Functional (8 parameters)

The unified torsion-energy functional bridging quantum to cosmological scales:

\`\`\`
Φ(T, S, K) = ∫ [α·T² + β·S·K + γ·∇T·∇T + δ·T⁴ + ε·R·T²] dV
\`\`\`

Physical constraints enforced:
- **Stability:** α > 0 (positive mass² term)
- **Causality:** v² = 2α/γ ≤ c² (subluminal propagation)
- **Unitarity:** δ > 0 (no ghost modes)
- **Energy conditions:** ρ ≥ 0 (weak energy condition)
- **Solar system:** |T₀| < 10⁻¹⁰ (observational bounds)

### 2.4 Torsion Wave Propagation (6 parameters)

Massive torsion field equation sampled at 50 spacetime points:

\`\`\`
□T + m²T + λT³ = J
\`\`\`

| Parameter | Range | Description |
|-----------|-------|-------------|
| mass | [0, 10⁻³ eV] | Torsion field mass |
| coupling | [-1, 1] | Quartic self-coupling |
| amplitude | [-10⁵, 10⁵] | Wave amplitude |
| frequency | [0.1, 100] | Angular frequency |
| phase | [0, 2π] | Phase offset |
| sourceStrength | [-10¹⁰, 10¹⁰] | Spin current source J |

---

## 3. Anomalies Detected

`;

  if (anomalies.length === 0) {
    report += `> No anomaly alerts recorded yet. The engines are still in early optimization cycles.
> Anomaly detection triggers when z-score outliers, landscape shifts, or
> constraint boundary violations are identified.

`;
  } else {
    report += `${anomalies.length} anomaly event(s) detected across both engines:\n\n`;
    for (let i = 0; i < anomalies.length; i++) {
      const a = anomalies[i];
      report += `### Anomaly ${i + 1}: ${a.title || 'Untitled'}

- **Severity:** ${(a.severity || 'unknown').toUpperCase()}
- **Time:** ${formatTimestamp(a.timestamp)}
- **Category:** ${a.category}
- **Detail:** ${a.detail || 'No additional detail.'}
`;
      if (a.data) {
        report += `- **Data:**\n`;
        for (const [k, v] of Object.entries(a.data)) {
          if (typeof v === 'object') {
            report += `  - ${k}: \`${JSON.stringify(v)}\`\n`;
          } else {
            report += `  - ${k}: ${v}\n`;
          }
        }
      }
      report += '\n';
    }
  }

  // ── Breakthroughs ──
  report += `## 4. Breakthroughs

`;
  if (breakthroughs.length === 0) {
    report += `> No breakthrough events yet. A breakthrough is triggered when a run achieves
> a score improvement exceeding the configured threshold relative to the prior
> best in that task domain.

`;
  } else {
    report += `${breakthroughs.length} breakthrough event(s):\n\n`;
    for (let i = 0; i < breakthroughs.length; i++) {
      const b = breakthroughs[i];
      report += `### Breakthrough ${i + 1}: ${b.title || 'Untitled'}

- **Severity:** ${(b.severity || 'unknown').toUpperCase()}
- **Time:** ${formatTimestamp(b.timestamp)}
- **Detail:** ${b.detail || 'No additional detail.'}
`;
      if (b.data) {
        report += `- **Data:**\n`;
        for (const [k, v] of Object.entries(b.data)) {
          if (typeof v === 'object') {
            report += `  - ${k}: \`${JSON.stringify(v)}\`\n`;
          } else {
            report += `  - ${k}: ${v}\n`;
          }
        }
      }
      report += '\n';
    }
  }

  // ── Best Results per Torsion Domain ──
  report += `## 5. Best Results by Torsion Domain

`;

  const domains = ['Einstein-Cartan', 'f(T) Gravity', 'UFE Torsion', 'Torsion Wave'];
  for (const domain of domains) {
    const domainRuns = allTorsionRuns.filter(r => classifyTorsionRun(r.id) === domain);
    if (domainRuns.length === 0) {
      report += `### ${domain}\n\n> No completed runs yet.\n\n`;
      continue;
    }

    // Find best run
    const completedRuns = domainRuns.filter(r => r.bestScore !== null);
    if (completedRuns.length === 0) {
      report += `### ${domain}\n\n> ${domainRuns.length} run(s) in progress, none completed.\n\n`;
      continue;
    }

    completedRuns.sort((a, b) => a.bestScore - b.bestScore);
    const best = completedRuns[0];

    report += `### ${domain}

| Metric | Value |
|--------|-------|
| Best cost (residual) | ${formatNumber(best.bestScore)} |
| Total evaluations | ${best.totalEvals} |
| Improvements found | ${best.improvements} |
| UFE ratio | ${best.ufe ? (best.ufe.ufeRatio * 100).toFixed(1) + '%' : 'N/A'} |
| Convergence velocity | ${best.ufe ? formatNumber(best.ufe.convergenceVelocity) : 'N/A'} |
| Runs completed | ${completedRuns.length} |

**Best parameters found:**

| Parameter | Value |
|-----------|-------|
`;
    if (best.bestParams) {
      for (const [k, v] of Object.entries(best.bestParams)) {
        report += `| ${k} | ${formatNumber(v)} |\n`;
      }
    }

    // Strategy effectiveness
    if (best.strategyWins && Object.keys(best.strategyWins).length > 0) {
      report += `\n**Strategy contributions** (improvement counts):\n\n`;
      const sorted = Object.entries(best.strategyWins).sort((a, b) => b[1] - a[1]);
      for (const [strat, wins] of sorted) {
        report += `- ${strat}: ${wins} improvements\n`;
      }
    }
    report += '\n';
  }

  // ── Insights ──
  report += `## 6. Key Insights

`;
  if (insights.length === 0) {
    report += `> Insight generation occurs as the engines accumulate sufficient data
> to identify strategy effectiveness patterns, phase transitions, and
> convergence behavior across torsion parameter spaces.

`;
  } else {
    for (let i = 0; i < Math.min(insights.length, 20); i++) {
      const ins = insights[i];
      report += `${i + 1}. **${ins.title || 'Insight'}** — ${ins.detail || ''}\n`;
    }
    report += '\n';
  }

  // ── Physical Interpretation ──
  report += `## 7. Physical Interpretation & Discussion

### 7.1 Einstein-Cartan Results

The optimizer searches for torsion tensor configurations satisfying the Cartan
equation T^a_{bc} + δ^a_b T_c − δ^a_c T_b = 8πG s^a_{bc}. Low residual values
indicate physically consistent spin-torsion coupling at the explored spin density
magnitudes. Results near zero residual suggest parameter regimes where torsion
naturally decouples — consistent with the experimental non-observation of torsion
at accessible energy scales.

**Key question:** Do any discovered configurations show anomalously low residuals
at unexpected spin densities? Such configurations could indicate previously
unidentified resonance conditions in spin-torsion coupling.

### 7.2 f(T) Gravity Cosmology

The f(T) task fits modified teleparallel gravity models to 21 H(z) data points
spanning z = 0 to z = 2.34. The chi-squared metric against observational data
directly measures compatibility with observed cosmic expansion history.

**Significance:** Any f(T) model achieving χ² < 21 (≈ 1 per data point) while
requiring fewer fine-tuned parameters than ΛCDM would constitute evidence for
torsion-based modifications to gravity. The Born-Infeld and logarithmic models
are of particular theoretical interest due to their UV-complete behavior.

### 7.3 UFE Torsion Functional

The unified functional Φ(T, S, K) bridges quantum spin-torsion coupling to
macroscopic spacetime torsion. Physical constraints (stability, causality,
unitarity, energy conditions, solar system bounds) dramatically restrict the
viable parameter space.

**Novel aspect:** The gradient energy term γ·∇T·∇T introduces a characteristic
length scale ℓ = √(γ/2α) for torsion field variations. Discovered values of
this scale could point to new physics at specific energy thresholds.

### 7.4 Torsion Wave Propagation

If torsion is massive (m > 0), it propagates as a Proca-like field with finite
range λ_C = ℏ/(mc). The optimizer's best-fit mass values directly predict the
torsion interaction range.

**Experimental testable:** A torsion mass in the range 10⁻⁶ to 10⁻³ eV
would produce measurable spin-dependent forces at laboratory scales (μm to mm
range), potentially detectable by torsion balance experiments or spin-polarized
test mass experiments.

---

## 8. Methodology Notes

### 8.1 Optimization Framework

Both AEGIS and Seeker implement adaptive meta-learning across 10 optimization
strategies. A multi-armed bandit selects strategies based on their empirical
improvement rates, with Thompson sampling to balance exploration of strategy
effectiveness. All runs use seeded Xoshiro256** PRNG for reproducibility.

### 8.2 UFE Tracking

Every function evaluation is classified as "useful" if it either:
- Improves the best-known score, OR
- Explores a novel region of parameter space (discretized grid)

The UFE ratio (useful/total) measures optimization efficiency. The AUCC
(Area Under Convergence Curve) provides a single-number summary of convergence
quality. Time-to-target metrics report evaluations needed to close 10%, 50%,
and 90% of the initial optimality gap.

### 8.3 Anomaly Detection

Anomalies are detected via:
- **Z-score outliers:** Evaluations with |z| > 3σ from running mean
- **Landscape shifts:** Sudden change in the score distribution
- **Constraint boundary clustering:** Solutions clustering at physical constraint boundaries
- **Strategy disruptions:** Unexpected strategy dominance shifts

### 8.4 Pincer Configuration

AEGIS and Seeker operate in opposite-end pincer mode:
- **AEGIS cycle 1:** Exploration-heavy profiles on easy tasks → exploitation-heavy on hard tasks
- **Seeker cycle 1:** Exploitation-heavy on easy tasks → exploration-heavy on hard tasks
- **Each subsequent cycle:** Engines swap direction

This ensures that every (task, strategy-profile) combination is covered from
both the exploration and exploitation perspectives.

---

## 9. Data Availability

All raw data is available via the live monitoring API:

| Endpoint | URL |
|----------|-----|
| AEGIS snapshot | http://localhost:5555/api/snapshot |
| AEGIS alerts | http://localhost:5555/api/alerts |
| Seeker snapshot | http://localhost:5556/api/snapshot |
| Seeker alerts | http://localhost:5556/api/alerts |
| AEGIS run detail | http://localhost:5555/api/run/:id |
| Seeker run detail | http://localhost:5556/api/run/:id |

Full convergence curves, UFE metrics, and parameter histories are available
per-run through the /api/run/:id endpoints.

---

## 10. References

1. Hehl, F.W. et al. (1976). "General relativity with spin and torsion."
   *Rev. Mod. Phys.* 48, 393.
2. Cai, Y.-F., Capozziello, S., et al. (2016). "f(T) teleparallel gravity
   and cosmology." *Rep. Prog. Phys.* 79, 106901.
3. Hammond, R.T. (2002). "Torsion gravity." *Rep. Prog. Phys.* 65, 599.
4. Shapiro, I.L. (2002). "Physical aspects of the space-time torsion."
   *Phys. Rep.* 357, 113.
5. Planck Collaboration (2018). "Planck 2018 results. VI. Cosmological
   parameters." *A&A* 641, A6.

---

*Report generated automatically by the AEGIS/Seeker Autonomous Discovery Framework.*
*Copyright © 2012-2026 Danny Lee Eldridge. All rights reserved.*
`;

  return report;
}

// ─── HTML wrapper ────────────────────────────────────────────────────────────

function wrapHTML(markdown) {
  // Basic markdown → HTML (headings, tables, bold, code blocks, blockquotes)
  let html = markdown;

  // Code blocks
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>');

  // Tables
  html = html.replace(/^\|(.+)\|\s*\n\|[-| :]+\|\s*\n((?:\|.+\|\s*\n)*)/gm, (match, header, body) => {
    const ths = header.split('|').map(h => `<th>${h.trim()}</th>`).join('');
    const rows = body.trim().split('\n').map(row => {
      const tds = row.replace(/^\||\|$/g, '').split('|').map(c => `<td>${c.trim()}</td>`).join('');
      return `<tr>${tds}</tr>`;
    }).join('\n');
    return `<table><thead><tr>${ths}</tr></thead><tbody>${rows}</tbody></table>\n`;
  });

  // Headings
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // Bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // Blockquotes
  html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');

  // Horizontal rules
  html = html.replace(/^---$/gm, '<hr>');

  // Line breaks → paragraphs (rough)
  html = html.replace(/\n\n/g, '</p><p>');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Torsion Field Theory — Anomaly Report</title>
<style>
  body {
    font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
    max-width: 900px; margin: 40px auto; padding: 0 20px;
    color: #1a1a1a; line-height: 1.7; background: #fefefe;
  }
  h1 { font-size: 1.8em; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
  h2 { font-size: 1.4em; color: #2c3e50; margin-top: 2em; border-bottom: 1px solid #bdc3c7; }
  h3 { font-size: 1.15em; color: #34495e; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th, td { border: 1px solid #bdc3c7; padding: 8px 12px; text-align: left; font-size: 0.9em; }
  th { background: #ecf0f1; font-weight: bold; }
  pre { background: #f8f9fa; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 0.85em; }
  code { font-family: 'Consolas', 'Courier New', monospace; }
  blockquote { border-left: 3px solid #3498db; padding: 8px 16px; margin: 1em 0; background: #f0f7ff; font-style: italic; }
  hr { border: none; border-top: 1px solid #ccc; margin: 2em 0; }
  @media print { body { max-width: 100%; } }
</style>
</head>
<body>
${html}
</body>
</html>`;
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const outIdx = args.indexOf('--out');
  const outFile = outIdx >= 0 ? args[outIdx + 1] : null;
  const format = args.includes('--format') ? args[args.indexOf('--format') + 1] : 'md';

  console.error('Fetching live data from AEGIS (5555) and Seeker (5556)...');
  const data = await gatherData();

  if (!data.aegisSnap && !data.seekerSnap) {
    console.error('WARNING: Neither engine is responding. Report will contain template structure only.');
  } else {
    const ae = data.aegisSnap?.summary;
    const se = data.seekerSnap?.summary;
    console.error(`AEGIS: ${ae ? ae.totalRuns + ' runs, ' + ae.totalEvals + ' evals' : 'offline'}`);
    console.error(`Seeker: ${se ? se.totalRuns + ' runs, ' + se.totalEvals + ' evals' : 'offline'}`);
  }

  let report = buildReport(data);

  if (format === 'html') {
    report = wrapHTML(report);
  }

  if (outFile) {
    const fullPath = path.resolve(outFile);
    fs.writeFileSync(fullPath, report, 'utf8');
    console.error(`Report written to: ${fullPath}`);
  } else {
    process.stdout.write(report);
  }
}

main().catch(err => {
  console.error('Error generating report:', err);
  process.exit(1);
});
