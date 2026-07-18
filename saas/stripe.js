/**
 * AEGIS Optimizer — Stripe Payment Integration
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Handles:
 * - Checkout session creation for subscription tiers
 * - Webhook processing (subscription lifecycle events)
 * - Usage metering for eval-count billing
 * - Customer/subscription management
 *
 * Environment variables required:
 *   STRIPE_SECRET_KEY      — sk_live_... or sk_test_...
 *   STRIPE_WEBHOOK_SECRET  — whsec_...
 *   STRIPE_PRICE_STARTER   — price_... (Starter tier)
 *   STRIPE_PRICE_PRO       — price_... (Pro tier)
 *   STRIPE_PRICE_ENTERPRISE — price_... (Enterprise tier)
 */

const crypto = require('crypto');

// ─── Configuration ───────────────────────────────────────
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY || '';
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET || '';

const PRICE_IDS = {
  starter:    process.env.STRIPE_PRICE_STARTER    || 'price_starter_placeholder',
  pro:        process.env.STRIPE_PRICE_PRO        || 'price_pro_placeholder',
  enterprise: process.env.STRIPE_PRICE_ENTERPRISE || 'price_enterprise_placeholder',
};

const TIER_LIMITS = {
  free:       { dailyEvals: 100,    dualEngine: false, priority: false },
  starter:    { dailyEvals: 10000,  dualEngine: false, priority: false },
  pro:        { dailyEvals: 100000, dualEngine: true,  priority: false },
  enterprise: { dailyEvals: Infinity, dualEngine: true, priority: true },
};

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';

// ─── In-memory store (replace with DB in production) ─────
const customers = new Map();   // apiKey → { customerId, tier, subscriptionId, dailyUsage, lastReset }
const pendingSessions = new Map(); // sessionId → { apiKey, tier }

// Initialize free tier for demo key
customers.set('demo-key-001', {
  customerId: null,
  tier: 'free',
  subscriptionId: null,
  dailyUsage: 0,
  lastReset: new Date().toISOString().slice(0, 10),
});

// ─── Stripe API helpers (no SDK dependency) ──────────────
async function stripeRequest(method, path, body) {
  if (!STRIPE_SECRET_KEY) {
    throw new Error('STRIPE_SECRET_KEY not configured');
  }

  const https = require('https');
  const data = body ? new URLSearchParams(flattenObject(body)).toString() : '';

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.stripe.com',
      port: 443,
      path: `/v1${path}`,
      method: method,
      headers: {
        'Authorization': `Bearer ${STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(data),
      },
    };

    const req = https.request(options, (res) => {
      let responseBody = '';
      res.on('data', chunk => responseBody += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(responseBody);
          if (res.statusCode >= 400) {
            reject(new Error(parsed.error ? parsed.error.message : `Stripe error ${res.statusCode}`));
          } else {
            resolve(parsed);
          }
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

// Flatten nested objects for URL-encoded params: { a: { b: 'c' } } → { 'a[b]': 'c' }
function flattenObject(obj, prefix = '') {
  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    const newKey = prefix ? `${prefix}[${key}]` : key;
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      Object.assign(result, flattenObject(value, newKey));
    } else {
      result[newKey] = String(value);
    }
  }
  return result;
}

// ─── Checkout ────────────────────────────────────────────
async function createCheckoutSession(apiKey, tier) {
  if (!PRICE_IDS[tier]) {
    throw new Error(`Invalid tier: ${tier}. Options: starter, pro, enterprise`);
  }

  const session = await stripeRequest('POST', '/checkout/sessions', {
    mode: 'subscription',
    'line_items[0][price]': PRICE_IDS[tier],
    'line_items[0][quantity]': 1,
    success_url: `${BASE_URL}/api/billing/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${BASE_URL}/api/billing/cancel`,
    metadata: { apiKey, tier },
  });

  pendingSessions.set(session.id, { apiKey, tier });

  return {
    checkoutUrl: session.url,
    sessionId: session.id,
  };
}

// ─── Billing Portal ──────────────────────────────────────
async function createPortalSession(apiKey) {
  const customer = customers.get(apiKey);
  if (!customer || !customer.customerId) {
    throw new Error('No subscription found for this API key');
  }

  const session = await stripeRequest('POST', '/billing_portal/sessions', {
    customer: customer.customerId,
    return_url: `${BASE_URL}/api/billing/portal-return`,
  });

  return { portalUrl: session.url };
}

// ─── Webhook Processing ─────────────────────────────────
function verifyWebhookSignature(payload, signature) {
  if (!STRIPE_WEBHOOK_SECRET) return true; // Skip in dev

  const parts = {};
  signature.split(',').forEach(pair => {
    const [k, v] = pair.split('=');
    parts[k] = v;
  });

  const timestamp = parts['t'];
  const expected = crypto
    .createHmac('sha256', STRIPE_WEBHOOK_SECRET)
    .update(`${timestamp}.${payload}`)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(parts['v1'] || '')
  );
}

function handleWebhookEvent(event) {
  const type = event.type;
  const data = event.data.object;

  switch (type) {
    case 'checkout.session.completed': {
      const { apiKey, tier } = data.metadata || {};
      if (apiKey && tier) {
        customers.set(apiKey, {
          customerId: data.customer,
          tier,
          subscriptionId: data.subscription,
          dailyUsage: 0,
          lastReset: new Date().toISOString().slice(0, 10),
        });
        console.log(`✅ Subscription activated: ${apiKey} → ${tier}`);
      }
      break;
    }

    case 'customer.subscription.updated': {
      // Find customer by subscription ID
      for (const [key, cust] of customers.entries()) {
        if (cust.subscriptionId === data.id) {
          const status = data.status;
          if (status === 'active') {
            console.log(`🔄 Subscription updated: ${key}`);
          } else if (status === 'past_due') {
            console.log(`⚠️  Payment past due: ${key}`);
          }
          break;
        }
      }
      break;
    }

    case 'customer.subscription.deleted': {
      for (const [key, cust] of customers.entries()) {
        if (cust.subscriptionId === data.id) {
          cust.tier = 'free';
          cust.subscriptionId = null;
          console.log(`❌ Subscription cancelled: ${key} → free`);
          break;
        }
      }
      break;
    }

    case 'invoice.payment_failed': {
      console.log(`❌ Payment failed for customer: ${data.customer}`);
      break;
    }

    default:
      // Unhandled event type
      break;
  }

  return { received: true };
}

// ─── Usage Metering ──────────────────────────────────────
function checkUsage(apiKey, evalCount) {
  let customer = customers.get(apiKey);

  // Auto-register unknown keys as free
  if (!customer) {
    customer = {
      customerId: null,
      tier: 'free',
      subscriptionId: null,
      dailyUsage: 0,
      lastReset: new Date().toISOString().slice(0, 10),
    };
    customers.set(apiKey, customer);
  }

  // Reset daily counter if new day
  const today = new Date().toISOString().slice(0, 10);
  if (customer.lastReset !== today) {
    customer.dailyUsage = 0;
    customer.lastReset = today;
  }

  const limits = TIER_LIMITS[customer.tier] || TIER_LIMITS.free;

  if (customer.dailyUsage + evalCount > limits.dailyEvals) {
    return {
      allowed: false,
      tier: customer.tier,
      used: customer.dailyUsage,
      limit: limits.dailyEvals,
      remaining: Math.max(0, limits.dailyEvals - customer.dailyUsage),
      upgradeUrl: `${BASE_URL}/api/billing/upgrade`,
    };
  }

  return {
    allowed: true,
    tier: customer.tier,
    used: customer.dailyUsage,
    limit: limits.dailyEvals,
    remaining: limits.dailyEvals - customer.dailyUsage - evalCount,
  };
}

function recordUsage(apiKey, evalCount) {
  const customer = customers.get(apiKey);
  if (customer) {
    customer.dailyUsage += evalCount;
  }
}

function canUseDualEngine(apiKey) {
  const customer = customers.get(apiKey);
  if (!customer) return false;
  const limits = TIER_LIMITS[customer.tier] || TIER_LIMITS.free;
  return limits.dualEngine;
}

function getCustomerTier(apiKey) {
  const customer = customers.get(apiKey);
  return customer ? customer.tier : 'free';
}

function getUsageInfo(apiKey) {
  const customer = customers.get(apiKey);
  if (!customer) return { tier: 'free', dailyUsage: 0, limits: TIER_LIMITS.free };
  return {
    tier: customer.tier,
    dailyUsage: customer.dailyUsage,
    limits: TIER_LIMITS[customer.tier],
    subscriptionId: customer.subscriptionId ? '****' + customer.subscriptionId.slice(-4) : null,
  };
}

// ─── Generate API Key ────────────────────────────────────
function generateApiKey() {
  return `aegis-${crypto.randomBytes(24).toString('hex')}`;
}

// ─── Billing Routes Handler ──────────────────────────────
async function handleBillingRoute(url, method, req, res, sendJSON) {
  // POST /api/billing/checkout — Create Stripe Checkout session
  if (url === '/api/billing/checkout' && method === 'POST') {
    try {
      const body = await parseBodyFromReq(req);
      const apiKey = extractApiKey(req);
      if (!apiKey) { sendJSON(res, 401, { error: 'API key required' }); return true; }
      const result = await createCheckoutSession(apiKey, body.tier);
      sendJSON(res, 200, result);
    } catch (err) {
      sendJSON(res, 400, { error: err.message });
    }
    return true;
  }

  // POST /api/billing/portal — Stripe Customer Portal
  if (url === '/api/billing/portal' && method === 'POST') {
    try {
      const apiKey = extractApiKey(req);
      if (!apiKey) { sendJSON(res, 401, { error: 'API key required' }); return true; }
      const result = await createPortalSession(apiKey);
      sendJSON(res, 200, result);
    } catch (err) {
      sendJSON(res, 400, { error: err.message });
    }
    return true;
  }

  // POST /api/billing/webhook — Stripe webhook
  if (url === '/api/billing/webhook' && method === 'POST') {
    try {
      const payload = await getRawBody(req);
      const sig = req.headers['stripe-signature'] || '';
      if (STRIPE_WEBHOOK_SECRET && !verifyWebhookSignature(payload, sig)) {
        sendJSON(res, 400, { error: 'Invalid webhook signature' });
        return true;
      }
      const event = JSON.parse(payload);
      const result = handleWebhookEvent(event);
      sendJSON(res, 200, result);
    } catch (err) {
      sendJSON(res, 400, { error: err.message });
    }
    return true;
  }

  // GET /api/billing/usage — Usage stats
  if (url === '/api/billing/usage' && method === 'GET') {
    const apiKey = extractApiKey(req);
    if (!apiKey) { sendJSON(res, 401, { error: 'API key required' }); return true; }
    sendJSON(res, 200, getUsageInfo(apiKey));
    return true;
  }

  // GET /api/billing/success — Post-checkout redirect
  if (url.startsWith('/api/billing/success') && method === 'GET') {
    sendJSON(res, 200, {
      status: 'success',
      message: 'Subscription activated! Your API key is now upgraded.',
    });
    return true;
  }

  // GET /api/billing/cancel — Cancelled checkout redirect
  if (url === '/api/billing/cancel' && method === 'GET') {
    sendJSON(res, 200, { status: 'cancelled', message: 'Checkout cancelled.' });
    return true;
  }

  // GET /api/billing/tiers — Show all pricing tiers
  if (url === '/api/billing/tiers' && method === 'GET') {
    sendJSON(res, 200, {
      tiers: [
        { name: 'Free',       price: '$0/mo',     dailyEvals: 100,     dualEngine: false, priority: false },
        { name: 'Starter',    price: '$99/mo',     dailyEvals: 10000,   dualEngine: false, priority: false },
        { name: 'Pro',        price: '$499/mo',    dailyEvals: 100000,  dualEngine: true,  priority: false },
        { name: 'Enterprise', price: '$5,000/mo',  dailyEvals: 'unlimited', dualEngine: true, priority: true },
      ],
    });
    return true;
  }

  // POST /api/billing/api-key — Generate new API key (would normally require auth)
  if (url === '/api/billing/api-key' && method === 'POST') {
    const newKey = generateApiKey();
    customers.set(newKey, {
      customerId: null,
      tier: 'free',
      subscriptionId: null,
      dailyUsage: 0,
      lastReset: new Date().toISOString().slice(0, 10),
    });
    sendJSON(res, 200, { apiKey: newKey, tier: 'free' });
    return true;
  }

  return false; // Not a billing route
}

// ─── Helpers ─────────────────────────────────────────────
function extractApiKey(req) {
  const auth = req.headers['authorization'] || '';
  return auth.replace('Bearer ', '') || null;
}

function parseBodyFromReq(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try { resolve(JSON.parse(body)); }
      catch (e) { reject(new Error('Invalid JSON')); }
    });
  });
}

function getRawBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => resolve(body));
    req.on('error', reject);
  });
}

module.exports = {
  handleBillingRoute,
  checkUsage,
  recordUsage,
  canUseDualEngine,
  getCustomerTier,
  getUsageInfo,
  generateApiKey,
  TIER_LIMITS,
};
