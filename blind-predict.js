'use strict';
// ─────────────────────────────────────────────────────────────────────────────
// BLIND PREDICTION TEST — Hold out DESI BAO, fit on CC+SNe, predict BAO
// This validates the torsion model can predict unseen data, not just fit it.
// ─────────────────────────────────────────────────────────────────────────────
const ufeTasks = require('./ufe-tasks');

const {
  torsionHubble, comovingDistance,
  CC_DATA, SNE_DATA, DESI_BAO,
  C_LIGHT, OMEGA_R0,
} = ufeTasks;

// ── Training objective: CC + SNe only (no BAO) ──────────────────────────────
function trainObjective(p) {
  let chi2 = 0;
  // Cosmic chronometers
  for (const d of CC_DATA) {
    const Hpred = torsionHubble(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
    chi2 += ((d.H - Hpred) / d.sigma) ** 2;
  }
  // SNe Ia
  for (const d of SNE_DATA) {
    const dL = (1 + d.z) * comovingDistance(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
    const mu_pred = 5 * Math.log10(Math.max(dL, 1e-10)) + 25;
    chi2 += ((d.mu - mu_pred) / d.sigma) ** 2;
  }
  // CMB angular scale prior (geometrical, not BAO-dependent)
  const DC_star = comovingDistance(1089, p.H0, p.omega_m, OMEGA_R0, p.beta, 1000);
  const theta_pred = p.rs / DC_star;
  const theta_obs = 0.010411;
  chi2 += ((theta_pred / theta_obs - 1) / 0.003) ** 2;
  return chi2;
}

const trainTask = {
  id: 'blind-train', name: 'Blind Training: CC+SNe+CMBθ* (no BAO)',
  evaluate: trainObjective,
  parameters: [
    { name: 'H0', min: 60, max: 80, description: 'Hubble constant' },
    { name: 'omega_m', min: 0.15, max: 0.45, description: 'Matter density' },
    { name: 'beta', min: -0.5, max: 0.5, description: 'Torsion coupling' },
    { name: 'rs', min: 130, max: 160, description: 'Sound horizon (Mpc)' },
  ],
};

// ── Run optimization ────────────────────────────────────────────────────────
async function runBlindTest() {
  const aegis = require('./dist/index.js');

  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║   BLIND PREDICTION TEST — Torsion Cosmology Validation     ║');
  console.log('╠══════════════════════════════════════════════════════════════╣');
  console.log('║  Training:   CC (29 points) + SNe (16 points) + CMB θ*     ║');
  console.log('║  Held out:   DESI BAO (6 distance measurements)            ║');
  console.log('║  Question:   Can torsion predict BAO distances it never    ║');
  console.log('║              saw during training?                          ║');
  console.log('╚══════════════════════════════════════════════════════════════╝\n');

  // Run multiple seeds for robustness
  const SEEDS = 10;
    const EVALS = 8000;
  const results = [];

  for (let s = 0; s < SEEDS; s++) {
    const agent = new aegis.AegisAgent(trainTask, {
      maxEvals: EVALS,
      seed: 42 + s * 7,
      verbosity: 'silent',
    });
    const result = await agent.run();
    if (result.best) {
      results.push(result.best);
      process.stdout.write(`  Seed ${s + 1}/${SEEDS}: chi²=${result.best.score.toFixed(2)}  H0=${result.best.params.H0.toFixed(2)}  Ωm=${result.best.params.omega_m.toFixed(3)}  β=${result.best.params.beta.toFixed(4)}\n`);
    }
  }

  // Pick the best fit
  results.sort((a, b) => a.score - b.score);
  const best = results[0].params;
  console.log(`\n  Best training fit: chi²=${results[0].score.toFixed(3)}`);
  console.log(`  H₀ = ${best.H0.toFixed(2)} km/s/Mpc`);
  console.log(`  Ωm = ${best.omega_m.toFixed(4)}`);
  console.log(`  β  = ${best.beta.toFixed(5)}`);
  console.log(`  rs = ${best.rs.toFixed(2)} Mpc\n`);

  // ── BLIND PREDICTION: compute BAO distances ─────────────────────────────
  console.log('  ┌─────────────────────────────────────────────────────────────┐');
  console.log('  │                   BLIND BAO PREDICTIONS                    │');
  console.log('  ├────────┬───────────┬───────────┬───────────┬───────────────┤');
  console.log('  │   z    │ Observed  │ Predicted │   Error   │   Tension     │');
  console.log('  ├────────┼───────────┼───────────┼───────────┼───────────────┤');

  let totalChi2 = 0;
  let nPredictions = 0;

  for (const d of DESI_BAO) {
    const DM = comovingDistance(d.z, best.H0, best.omega_m, OMEGA_R0, best.beta);
    const DH = C_LIGHT / torsionHubble(d.z, best.H0, best.omega_m, OMEGA_R0, best.beta);

    // Use the fitted sound horizon from training (not hardcoded)
    const rs = best.rs;

    if (d.DV_rs) {
      const DV = Math.pow(d.z * DM * DM * DH, 1 / 3);
      const pred = DV / rs;
      const pull = (pred - d.DV_rs) / d.sigma;
      const chi2 = pull * pull;
      totalChi2 += chi2;
      nPredictions++;
      const status = Math.abs(pull) < 1 ? '  ✓ <1σ  ' : Math.abs(pull) < 2 ? '  ~ 1-2σ ' : '  ✗ >2σ  ';
      console.log(`  │ ${d.z.toFixed(3)}  │ ${d.DV_rs.toFixed(3).padStart(7)}±${d.sigma} │ ${pred.toFixed(3).padStart(7)}   │ ${pull.toFixed(2).padStart(6)}σ   │${status}     │`);
    }
    if (d.DM_rs) {
      const pred = DM / rs;
      const pull = (pred - d.DM_rs) / d.sigma;
      const chi2 = pull * pull;
      totalChi2 += chi2;
      nPredictions++;
      const status = Math.abs(pull) < 1 ? '  ✓ <1σ  ' : Math.abs(pull) < 2 ? '  ~ 1-2σ ' : '  ✗ >2σ  ';
      console.log(`  │ ${d.z.toFixed(3)}  │ ${d.DM_rs.toFixed(3).padStart(7)}±${d.sigma} │ ${pred.toFixed(3).padStart(7)}   │ ${pull.toFixed(2).padStart(6)}σ   │${status}     │`);
    }
    if (d.DH_rs) {
      const pred = DH / rs;
      const pull = (pred - d.DH_rs) / d.DH_sig;
      const chi2 = pull * pull;
      totalChi2 += chi2;
      nPredictions++;
      const status = Math.abs(pull) < 1 ? '  ✓ <1σ  ' : Math.abs(pull) < 2 ? '  ~ 1-2σ ' : '  ✗ >2σ  ';
      console.log(`  │ ${d.z.toFixed(3)}  │ ${d.DH_rs.toFixed(3).padStart(7)}±${d.DH_sig} │ ${pred.toFixed(3).padStart(7)}   │ ${pull.toFixed(2).padStart(6)}σ   │${status}     │`);
    }
  }

  console.log('  └────────┴───────────┴───────────┴───────────┴───────────────┘');
  console.log(`\n  Total blind prediction chi²: ${totalChi2.toFixed(2)} (${nPredictions} predictions)`);
  console.log(`  Reduced chi²: ${(totalChi2 / nPredictions).toFixed(3)} (expected ~1.0 for good model)\n`);

  // ── Verdict ─────────────────────────────────────────────────────────────
  const reduced = totalChi2 / nPredictions;
  if (reduced < 2.0) {
    console.log('  VERDICT: ✓ PASS — Torsion model successfully predicts unseen BAO data');
    console.log('           The model has genuine predictive power, not just curve-fitting.\n');
  } else if (reduced < 5.0) {
    console.log('  VERDICT: ~ MARGINAL — Some tension with unseen BAO data');
    console.log('           Model may need refinement or additional parameters.\n');
  } else {
    console.log('  VERDICT: ✗ FAIL — Model cannot predict unseen BAO data');
    console.log('           Overfitting or missing physics suspected.\n');
  }

  // ── ΛCDM comparison ────────────────────────────────────────────────────
  console.log('  ── ΛCDM Comparison (β=0) ──');
  const lcdm = { H0: 67.4, omega_m: 0.315, beta: 0 };
  let lcdmChi2 = 0;
  for (const d of DESI_BAO) {
    const DM = comovingDistance(d.z, lcdm.H0, lcdm.omega_m, OMEGA_R0, 0);
    const DH = C_LIGHT / torsionHubble(d.z, lcdm.H0, lcdm.omega_m, OMEGA_R0, 0);
    const rs = 147.09;
    if (d.DV_rs) { const p = (Math.pow(d.z*DM*DM*DH,1/3)/rs - d.DV_rs)/d.sigma; lcdmChi2 += p*p; }
    if (d.DM_rs) { const p = (DM/rs - d.DM_rs)/d.sigma; lcdmChi2 += p*p; }
    if (d.DH_rs) { const p = (DH/rs - d.DH_rs)/d.DH_sig; lcdmChi2 += p*p; }
  }
  console.log(`  ΛCDM BAO chi²: ${lcdmChi2.toFixed(2)} (reduced: ${(lcdmChi2/nPredictions).toFixed(3)})`);
  console.log(`  Torsion BAO chi²: ${totalChi2.toFixed(2)} (reduced: ${(totalChi2/nPredictions).toFixed(3)})`);
  if (totalChi2 < lcdmChi2) {
    console.log(`  → Torsion outperforms ΛCDM by Δχ²=${(lcdmChi2-totalChi2).toFixed(2)}\n`);
  } else {
    console.log(`  → ΛCDM outperforms torsion by Δχ²=${(totalChi2-lcdmChi2).toFixed(2)}\n`);
  }
}

runBlindTest().catch(e => console.error(e));
