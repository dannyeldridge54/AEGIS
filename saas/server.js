/**
 * AEGIS Optimizer — SaaS API Server
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * REST API for cloud-hosted optimization.
 * POST /api/optimize — single engine
 * POST /api/dual-optimize — dual engine with cross-pollination
 * GET  /api/status/:jobId — check job status
 * GET  /api/result/:jobId — get results
 * GET  /api/health — health check
 */

const http = require('http');
const { optimize, dualOptimize } = require('../sdk/index');
const billing = require('./stripe');

const PORT = process.env.PORT || 3000;
const API_KEYS = new Set((process.env.API_KEYS || 'demo-key-001').split(','));

// In-memory job store (replace with Redis/DB in production)
const jobs = new Map();
let jobCounter = 0;

function generateJobId() {
  return `job-${++jobCounter}-${Date.now().toString(36)}`;
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try { resolve(JSON.parse(body)); }
      catch (e) { reject(new Error('Invalid JSON')); }
    });
  });
}

function sendJSON(res, status, data) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  });
  res.end(JSON.stringify(data));
}

function authenticate(req) {
  const auth = req.headers['authorization'] || '';
  const key = auth.replace('Bearer ', '');
  return API_KEYS.has(key);
}

// Build evaluate function from string (sandboxed)
function buildEvaluator(code) {
  // Only allow math operations — no require, process, fs, etc.
  const forbidden = ['require', 'process', 'import', 'eval', 'Function', 'fs', 'child_process', 'exec', 'spawn'];
  for (const f of forbidden) {
    if (code.includes(f)) throw new Error(`Forbidden token: ${f}`);
  }
  return new Function('params', `"use strict"; const p = params; ${code}`);
}

async function handleRequest(req, res) {
  const url = req.url;
  const method = req.method;

  // CORS preflight
  if (method === 'OPTIONS') {
    sendJSON(res, 200, {});
    return;
  }

  // Billing routes (Stripe checkout, webhook, usage, tiers)
  if (url.startsWith('/api/billing')) {
    const handled = await billing.handleBillingRoute(url, method, req, res, sendJSON);
    if (handled) return;
  }

  // Health check
  if (url === '/api/health' && method === 'GET') {
    sendJSON(res, 200, {
      status: 'ok',
      engine: 'AEGIS Optimizer',
      version: '1.0.0',
      activeJobs: [...jobs.values()].filter(j => j.status === 'running').length,
      totalJobs: jobs.size,
      uptime: process.uptime(),
    });
    return;
  }

  // Pricing / info
  if (url === '/api/info' && method === 'GET') {
    sendJSON(res, 200, {
      name: 'AEGIS Optimizer API',
      version: '1.0.0',
      author: 'Danny Lee Eldridge',
      endpoints: {
        'POST /api/optimize': 'Single-engine optimization',
        'POST /api/dual-optimize': 'Dual-engine with cross-pollination',
        'GET /api/status/:jobId': 'Check job status',
        'GET /api/result/:jobId': 'Get job results',
        'GET /api/health': 'Health check',
      },
      pricing: {
        free: '100 evaluations/day',
        starter: '$99/mo — 10,000 evals/day',
        pro: '$499/mo — 100,000 evals/day, dual engine',
        enterprise: '$5,000/mo — unlimited, priority, SLA',
      },
      strategies: ['random', 'evolutionary', 'gradient', 'annealing', 'swarm', 'curiosity', 'exploit'],
    });
    return;
  }

  // Auth required for optimization endpoints
  if (url.startsWith('/api/optimize') || url.startsWith('/api/dual-optimize')) {
    if (!authenticate(req)) {
      sendJSON(res, 401, { error: 'Invalid API key. Set Authorization: Bearer <key>' });
      return;
    }
  }

  // POST /api/optimize
  if (url === '/api/optimize' && method === 'POST') {
    try {
      const body = await parseBody(req);

      if (!body.objective || !body.parameters) {
        sendJSON(res, 400, { error: 'Missing required fields: objective (string), parameters (array)' });
        return;
      }

      const apiKey = (req.headers['authorization'] || '').replace('Bearer ', '');
      const evalCount = Math.min(body.maxEvals || 5000, 50000);

      // Check usage limits
      const usage = billing.checkUsage(apiKey, evalCount);
      if (!usage.allowed) {
        sendJSON(res, 429, {
          error: 'Daily evaluation limit reached',
          tier: usage.tier,
          used: usage.used,
          limit: usage.limit,
          upgradeUrl: usage.upgradeUrl,
        });
        return;
      }

      const jobId = generateJobId();
      const evaluator = buildEvaluator(body.objective);

      jobs.set(jobId, {
        id: jobId,
        type: 'single',
        status: 'running',
        created: new Date().toISOString(),
        result: null,
      });

      sendJSON(res, 202, { jobId, status: 'running', message: 'Optimization started', tier: usage.tier, remaining: usage.remaining });

      // Run async
      optimize({
        objective: evaluator,
        parameters: body.parameters,
        constraints: body.constraints,
        maxEvals: evalCount,
        explorationRate: body.explorationRate || 0.5,
        strategies: body.strategies,
        name: body.name || 'API Optimization',
      }).then(result => {
        billing.recordUsage(apiKey, evalCount);
        jobs.set(jobId, { ...jobs.get(jobId), status: 'completed', result, completed: new Date().toISOString() });
      }).catch(err => {
        jobs.set(jobId, { ...jobs.get(jobId), status: 'failed', error: err.message });
      });
    } catch (err) {
      sendJSON(res, 400, { error: err.message });
    }
    return;
  }

  // POST /api/dual-optimize
  if (url === '/api/dual-optimize' && method === 'POST') {
    try {
      const body = await parseBody(req);

      if (!body.objective || !body.parameters) {
        sendJSON(res, 400, { error: 'Missing required fields: objective (string), parameters (array)' });
        return;
      }

      const apiKey = (req.headers['authorization'] || '').replace('Bearer ', '');

      // Dual engine requires Pro tier or higher
      if (!billing.canUseDualEngine(apiKey)) {
        sendJSON(res, 403, {
          error: 'Dual-engine optimization requires Pro tier or higher',
          currentTier: billing.getCustomerTier(apiKey),
          upgradeUrl: `${process.env.BASE_URL || 'http://localhost:3000'}/api/billing/checkout`,
        });
        return;
      }

      const evalCount = Math.min(body.maxEvals || 3000, 30000) * 2; // dual uses 2x
      const usage = billing.checkUsage(apiKey, evalCount);
      if (!usage.allowed) {
        sendJSON(res, 429, {
          error: 'Daily evaluation limit reached',
          tier: usage.tier,
          used: usage.used,
          limit: usage.limit,
        });
        return;
      }

      const jobId = generateJobId();
      const evaluator = buildEvaluator(body.objective);

      jobs.set(jobId, {
        id: jobId,
        type: 'dual',
        status: 'running',
        created: new Date().toISOString(),
        result: null,
      });

      sendJSON(res, 202, { jobId, status: 'running', message: 'Dual optimization started', tier: usage.tier });

      dualOptimize({
        objective: evaluator,
        parameters: body.parameters,
        constraints: body.constraints,
        maxEvals: Math.min(body.maxEvals || 3000, 30000),
        cycles: Math.min(body.cycles || 5, 20),
        name: body.name || 'API Dual Optimization',
      }).then(result => {
        billing.recordUsage(apiKey, evalCount);
        jobs.set(jobId, { ...jobs.get(jobId), status: 'completed', result, completed: new Date().toISOString() });
      }).catch(err => {
        jobs.set(jobId, { ...jobs.get(jobId), status: 'failed', error: err.message });
      });
    } catch (err) {
      sendJSON(res, 400, { error: err.message });
    }
    return;
  }

  // GET /api/status/:jobId
  if (url.startsWith('/api/status/') && method === 'GET') {
    const jobId = url.split('/api/status/')[1];
    const job = jobs.get(jobId);
    if (!job) { sendJSON(res, 404, { error: 'Job not found' }); return; }
    sendJSON(res, 200, { id: job.id, type: job.type, status: job.status, created: job.created });
    return;
  }

  // GET /api/result/:jobId
  if (url.startsWith('/api/result/') && method === 'GET') {
    const jobId = url.split('/api/result/')[1];
    const job = jobs.get(jobId);
    if (!job) { sendJSON(res, 404, { error: 'Job not found' }); return; }
    if (job.status === 'running') { sendJSON(res, 202, { status: 'running', message: 'Still optimizing...' }); return; }
    if (job.status === 'failed') { sendJSON(res, 500, { status: 'failed', error: job.error }); return; }
    sendJSON(res, 200, { status: 'completed', ...job.result, created: job.created, completed: job.completed });
    return;
  }

  // Fallback
  sendJSON(res, 404, { error: 'Not found. See GET /api/info for available endpoints.' });
}

const server = http.createServer(handleRequest);
server.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════╗
║   AEGIS Optimizer — SaaS API Server                  ║
║                                                       ║
║   http://localhost:${PORT}                              ║
║                                                       ║
║   Endpoints:                                          ║
║     POST /api/optimize        — single engine         ║
║     POST /api/dual-optimize   — dual + pollination    ║
║     GET  /api/status/:id      — job status            ║
║     GET  /api/result/:id      — job results           ║
║     GET  /api/health          — health check          ║
║     GET  /api/info            — pricing + docs        ║
║                                                       ║
║   Billing (Stripe):                                   ║
║     POST /api/billing/checkout  — start subscription  ║
║     POST /api/billing/webhook   — Stripe events       ║
║     GET  /api/billing/usage     — usage stats         ║
║     GET  /api/billing/tiers     — pricing tiers       ║
║     POST /api/billing/api-key   — generate API key    ║
║                                                       ║
║   Auth: Authorization: Bearer <api-key>               ║
╚═══════════════════════════════════════════════════════╝
  `);
});
