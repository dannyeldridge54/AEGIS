"use strict";
/**
 * AEGIS — Real-World Data Connectors
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Live data feeds from real physical/financial/scientific sources.
 * Zero dependencies — uses Node's built-in http/https.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.live = exports.math = exports.engineering = exports.environment = exports.finance = exports.physics = void 0;
const https = __importStar(require("https"));
const http = __importStar(require("http"));
// ─── Generic HTTP Fetcher ────────────────────────────────────────────────────
function fetchJSON(url, headers) {
    return new Promise((resolve, reject) => {
        const parsed = new URL(url);
        const lib = parsed.protocol === 'https:' ? https : http;
        lib.get(url, { headers: headers || {} }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                }
                catch {
                    reject(new Error(`Failed to parse: ${data.slice(0, 200)}`));
                }
            });
        }).on('error', reject);
    });
}
function fetchText(url) {
    return new Promise((resolve, reject) => {
        const parsed = new URL(url);
        const lib = parsed.protocol === 'https:' ? https : http;
        lib.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve(data));
        }).on('error', reject);
    });
}
// ─── Physics & Cosmology Data ────────────────────────────────────────────────
exports.physics = {
    /** NIST physical constants (2022 CODATA) */
    constants: {
        c: 299792458, // speed of light (m/s)
        h: 6.62607015e-34, // Planck constant (J·s)
        hbar: 1.054571817e-34, // reduced Planck (J·s)
        G: 6.67430e-11, // gravitational constant (m³/kg/s²)
        k_B: 1.380649e-23, // Boltzmann constant (J/K)
        e: 1.602176634e-19, // electron charge (C)
        m_e: 9.1093837015e-31, // electron mass (kg)
        m_p: 1.67262192369e-27, // proton mass (kg)
        N_A: 6.02214076e23, // Avogadro number
        sigma: 5.670374419e-8, // Stefan-Boltzmann (W/m²/K⁴)
        alpha: 7.2973525693e-3, // fine structure constant
        R_inf: 10973731.568160, // Rydberg constant (1/m)
        mu_0: 1.25663706212e-6, // vacuum permeability (N/A²)
        epsilon_0: 8.8541878128e-12, // vacuum permittivity (F/m)
        // Cosmological
        H0_planck: 67.4, // Hubble constant Planck 2018 (km/s/Mpc)
        H0_shoes: 73.04, // Hubble constant SH0ES 2022 (km/s/Mpc)
        Omega_m: 0.315, // Matter density Planck 2018
        Omega_b: 0.0493, // Baryon density Planck 2018
        Omega_Lambda: 0.685, // Dark energy density
        T_cmb: 2.7255, // CMB temperature (K)
        t_universe: 13.797e9, // Age of universe (years)
        sigma_8: 0.811, // Matter fluctuation amplitude
        n_s: 0.9649, // Scalar spectral index
    },
    /** Hubble rate measurements (z, H(z) km/s/Mpc, σ) — cosmic chronometers */
    hubbleData: [
        { z: 0.07, H: 69.0, sigma: 19.6 },
        { z: 0.09, H: 69.0, sigma: 12.0 },
        { z: 0.12, H: 68.6, sigma: 26.2 },
        { z: 0.17, H: 83.0, sigma: 8.0 },
        { z: 0.179, H: 75.0, sigma: 4.0 },
        { z: 0.199, H: 75.0, sigma: 5.0 },
        { z: 0.2, H: 72.9, sigma: 29.6 },
        { z: 0.27, H: 77.0, sigma: 14.0 },
        { z: 0.28, H: 88.8, sigma: 36.6 },
        { z: 0.352, H: 83.0, sigma: 14.0 },
        { z: 0.3802, H: 83.0, sigma: 13.5 },
        { z: 0.4, H: 95.0, sigma: 17.0 },
        { z: 0.4004, H: 77.0, sigma: 10.2 },
        { z: 0.4247, H: 87.1, sigma: 11.2 },
        { z: 0.4497, H: 92.8, sigma: 12.9 },
        { z: 0.47, H: 89.0, sigma: 49.6 },
        { z: 0.4783, H: 80.9, sigma: 9.0 },
        { z: 0.48, H: 97.0, sigma: 62.0 },
        { z: 0.593, H: 104.0, sigma: 13.0 },
        { z: 0.68, H: 92.0, sigma: 8.0 },
        { z: 0.781, H: 105.0, sigma: 12.0 },
        { z: 0.875, H: 125.0, sigma: 17.0 },
        { z: 0.88, H: 90.0, sigma: 40.0 },
        { z: 0.9, H: 117.0, sigma: 23.0 },
        { z: 1.037, H: 154.0, sigma: 20.0 },
        { z: 1.3, H: 168.0, sigma: 17.0 },
        { z: 1.363, H: 160.0, sigma: 33.6 },
        { z: 1.43, H: 177.0, sigma: 18.0 },
        { z: 1.53, H: 140.0, sigma: 14.0 },
        { z: 1.75, H: 202.0, sigma: 40.0 },
        { z: 1.965, H: 186.5, sigma: 50.4 },
    ],
    /** BAO measurements (DESI DR1 2024 + SDSS) */
    baoData: [
        // DESI DR1 (2024)
        { z: 0.295, DV_rd: 7.93, sigma: 0.15, source: 'DESI-BGS' },
        { z: 0.510, DM_rd: 13.62, sigma: 0.25, DH_rd: 20.98, DH_sigma: 0.61, source: 'DESI-LRG1' },
        { z: 0.706, DM_rd: 16.85, sigma: 0.32, DH_rd: 20.08, DH_sigma: 0.60, source: 'DESI-LRG2' },
        { z: 0.930, DM_rd: 21.71, sigma: 0.28, DH_rd: 17.88, DH_sigma: 0.35, source: 'DESI-LRG3+ELG1' },
        { z: 1.317, DM_rd: 27.79, sigma: 0.69, DH_rd: 13.82, DH_sigma: 0.42, source: 'DESI-ELG2' },
        { z: 1.491, DM_rd: 30.69, sigma: 1.00, DH_rd: 13.23, DH_sigma: 0.48, source: 'DESI-QSO' },
        { z: 2.330, DM_rd: 39.71, sigma: 0.94, DH_rd: 8.52, DH_sigma: 0.17, source: 'DESI-LyA' },
        // SDSS/eBOSS (legacy)
        { z: 0.38, DM_rd: 10.27, sigma: 0.15, DH_rd: 25.00, DH_sigma: 0.76, source: 'SDSS-BOSS' },
        { z: 0.51, DM_rd: 13.38, sigma: 0.18, DH_rd: 22.33, DH_sigma: 0.58, source: 'SDSS-BOSS' },
        { z: 0.61, DM_rd: 15.45, sigma: 0.20, DH_rd: 20.57, DH_sigma: 0.49, source: 'SDSS-BOSS' },
        { z: 1.48, DM_rd: 30.21, sigma: 0.79, DH_rd: 13.23, DH_sigma: 0.47, source: 'SDSS-eBOSS-QSO' },
        { z: 2.33, DM_rd: 37.6, sigma: 1.2, DH_rd: 8.93, DH_sigma: 0.28, source: 'SDSS-eBOSS-LyA' },
    ],
    /** Type Ia Supernovae (Pantheon+ binned, 20 bins) */
    sneData: [
        { z: 0.01, mu: 33.08, sigma: 0.07 },
        { z: 0.02, mu: 34.62, sigma: 0.04 },
        { z: 0.03, mu: 35.53, sigma: 0.03 },
        { z: 0.05, mu: 36.63, sigma: 0.02 },
        { z: 0.07, mu: 37.30, sigma: 0.02 },
        { z: 0.10, mu: 38.10, sigma: 0.02 },
        { z: 0.15, mu: 39.05, sigma: 0.02 },
        { z: 0.20, mu: 39.73, sigma: 0.02 },
        { z: 0.30, mu: 40.75, sigma: 0.02 },
        { z: 0.40, mu: 41.48, sigma: 0.02 },
        { z: 0.50, mu: 42.07, sigma: 0.03 },
        { z: 0.60, mu: 42.54, sigma: 0.03 },
        { z: 0.70, mu: 42.93, sigma: 0.04 },
        { z: 0.80, mu: 43.27, sigma: 0.05 },
        { z: 0.90, mu: 43.56, sigma: 0.06 },
        { z: 1.00, mu: 43.81, sigma: 0.06 },
        { z: 1.20, mu: 44.22, sigma: 0.07 },
        { z: 1.40, mu: 44.53, sigma: 0.10 },
        { z: 1.60, mu: 44.79, sigma: 0.14 },
        { z: 1.90, mu: 45.07, sigma: 0.20 },
    ],
    /** CMB acoustic scale and shift parameter (Planck 2018) */
    cmbData: {
        R_shift: { value: 1.7502, sigma: 0.0046 }, // CMB shift parameter
        l_A: { value: 301.471, sigma: 0.090 }, // Acoustic scale
        omega_b: { value: 0.02237, sigma: 0.00015 }, // Physical baryon density
        n_s: { value: 0.9649, sigma: 0.0042 }, // Scalar index
        z_star: 1089.92, // Redshift of last scattering
        r_star: 144.43, // Sound horizon at z* (Mpc)
        theta_star: 0.010411, // Angular scale
    },
    /** H₀ measurements from different methods */
    h0Measurements: [
        { value: 67.4, sigma: 0.5, method: 'Planck CMB 2018', source: 'Planck Collaboration' },
        { value: 73.04, sigma: 1.04, method: 'Cepheid-SN distance ladder', source: 'SH0ES (Riess+ 2022)' },
        { value: 69.8, sigma: 1.7, method: 'TRGB distance ladder', source: 'Freedman+ 2021' },
        { value: 67.6, sigma: 4.3, method: 'Gravitational wave sirens', source: 'LIGO/Virgo 2021' },
        { value: 73.3, sigma: 1.7, method: 'Strong gravitational lensing', source: 'H0LiCOW 2020' },
        { value: 68.3, sigma: 1.5, method: 'BAO + BBN', source: 'DESI 2024' },
        { value: 72.1, sigma: 2.0, method: 'Surface brightness fluctuations', source: 'Khetan+ 2021' },
    ],
    /** Growth rate f·σ₈ measurements */
    growthData: [
        { z: 0.02, fsigma8: 0.398, sigma: 0.065 },
        { z: 0.067, fsigma8: 0.423, sigma: 0.055 },
        { z: 0.10, fsigma8: 0.370, sigma: 0.130 },
        { z: 0.17, fsigma8: 0.510, sigma: 0.060 },
        { z: 0.22, fsigma8: 0.420, sigma: 0.070 },
        { z: 0.25, fsigma8: 0.351, sigma: 0.058 },
        { z: 0.35, fsigma8: 0.440, sigma: 0.050 },
        { z: 0.37, fsigma8: 0.460, sigma: 0.038 },
        { z: 0.44, fsigma8: 0.413, sigma: 0.080 },
        { z: 0.57, fsigma8: 0.441, sigma: 0.043 },
        { z: 0.60, fsigma8: 0.390, sigma: 0.063 },
        { z: 0.73, fsigma8: 0.437, sigma: 0.072 },
        { z: 0.80, fsigma8: 0.470, sigma: 0.080 },
        { z: 1.05, fsigma8: 0.280, sigma: 0.080 },
        { z: 1.40, fsigma8: 0.482, sigma: 0.116 },
        { z: 1.52, fsigma8: 0.420, sigma: 0.076 },
    ],
};
// ─── Financial Market Data ───────────────────────────────────────────────────
exports.finance = {
    /** Fetch live stock/crypto price (no API key needed — uses free endpoints) */
    async getPrice(symbol) {
        try {
            // Try Yahoo Finance API (no key needed)
            const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1d&range=1d`;
            const data = await fetchJSON(url);
            const result = data?.chart?.result?.[0];
            if (!result)
                return null;
            const meta = result.meta;
            return {
                price: meta.regularMarketPrice,
                change: ((meta.regularMarketPrice - meta.previousClose) / meta.previousClose) * 100,
                volume: meta.regularMarketVolume || 0,
            };
        }
        catch {
            return null;
        }
    },
    /** Common benchmark rates */
    rates: {
        fed_funds: 5.33, // Federal Funds Rate (2024)
        us_10y: 4.25, // US 10-year Treasury yield
        inflation_cpi: 3.2, // US CPI year-over-year
        sp500_pe: 28.5, // S&P 500 P/E ratio
    },
};
// ─── Weather & Environmental ─────────────────────────────────────────────────
exports.environment = {
    /** Fetch current weather (Open-Meteo, no API key) */
    async getWeather(lat, lon) {
        try {
            const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code`;
            const data = await fetchJSON(url);
            const current = data.current;
            return {
                temperature: current.temperature_2m,
                windSpeed: current.wind_speed_10m,
                humidity: current.relative_humidity_2m,
                description: weatherCodeToString(current.weather_code),
            };
        }
        catch {
            return null;
        }
    },
    /** Global climate data (key metrics) */
    climate: {
        co2_ppm_2024: 421.5, // Atmospheric CO2 (Mauna Loa)
        global_temp_anomaly: 1.45, // °C above pre-industrial (2024)
        sea_level_rise_mm_yr: 3.7, // Current rate
        arctic_ice_km2: 4.23e6, // September minimum (2024)
        ocean_ph: 8.05, // Surface ocean pH (declining)
    },
};
function weatherCodeToString(code) {
    if (code === 0)
        return 'Clear sky';
    if (code <= 3)
        return 'Partly cloudy';
    if (code <= 48)
        return 'Fog';
    if (code <= 57)
        return 'Drizzle';
    if (code <= 67)
        return 'Rain';
    if (code <= 77)
        return 'Snow';
    if (code <= 82)
        return 'Rain showers';
    if (code <= 86)
        return 'Snow showers';
    if (code >= 95)
        return 'Thunderstorm';
    return 'Unknown';
}
// ─── Engineering & Materials ─────────────────────────────────────────────────
exports.engineering = {
    /** Common material properties */
    materials: {
        steel_A36: { density: 7850, yield_MPa: 250, E_GPa: 200, poisson: 0.26 },
        aluminum_6061: { density: 2700, yield_MPa: 276, E_GPa: 68.9, poisson: 0.33 },
        titanium_Ti6Al4V: { density: 4430, yield_MPa: 880, E_GPa: 113.8, poisson: 0.342 },
        concrete_C30: { density: 2400, compressive_MPa: 30, E_GPa: 33, poisson: 0.2 },
        carbon_fiber: { density: 1600, tensile_MPa: 3500, E_GPa: 230, poisson: 0.27 },
        copper: { density: 8960, yield_MPa: 70, E_GPa: 110, conductivity_S_m: 5.96e7 },
        glass: { density: 2500, tensile_MPa: 33, E_GPa: 70, poisson: 0.22 },
    },
    /** Standard atmosphere (ISA) at altitude */
    atmosphere(altitude_m) {
        const T0 = 288.15, P0 = 101325, rho0 = 1.225;
        const L = 0.0065; // lapse rate K/m
        const g = 9.80665, M = 0.0289644, R = 8.31447;
        if (altitude_m <= 11000) {
            const T = T0 - L * altitude_m;
            const P = P0 * Math.pow(T / T0, g * M / (R * L));
            const rho = rho0 * Math.pow(T / T0, (g * M / (R * L)) - 1);
            return { temperature_K: T, pressure_Pa: P, density_kg_m3: rho };
        }
        else {
            // Stratosphere (isothermal ~216.65K up to 20km)
            const T11 = 216.65;
            const P11 = P0 * Math.pow(T11 / T0, g * M / (R * L));
            const P = P11 * Math.exp(-g * M * (altitude_m - 11000) / (R * T11));
            const rho = P * M / (R * T11);
            return { temperature_K: T11, pressure_Pa: P, density_kg_m3: rho };
        }
    },
    /** Orbital mechanics */
    orbital: {
        earth_radius_km: 6371,
        earth_mass_kg: 5.972e24,
        mu_earth: 3.986e14, // GM (m³/s²)
        LEO_velocity_km_s: 7.8,
        GEO_altitude_km: 35786,
        escape_velocity_km_s: 11.2,
        /** Orbital velocity at given altitude */
        velocity(altitude_km) {
            const r = (6371 + altitude_km) * 1000;
            return Math.sqrt(3.986e14 / r) / 1000; // km/s
        },
        /** Orbital period at given altitude */
        period(altitude_km) {
            const r = (6371 + altitude_km) * 1000;
            return 2 * Math.PI * Math.sqrt(r ** 3 / 3.986e14); // seconds
        },
    },
};
// ─── Math & Statistics Utilities ─────────────────────────────────────────────
exports.math = {
    /** Standard statistical functions */
    mean(data) {
        return data.reduce((a, b) => a + b, 0) / data.length;
    },
    std(data) {
        const m = exports.math.mean(data);
        return Math.sqrt(data.reduce((s, x) => s + (x - m) ** 2, 0) / (data.length - 1));
    },
    median(data) {
        const sorted = [...data].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
    },
    percentile(data, p) {
        const sorted = [...data].sort((a, b) => a - b);
        const idx = (p / 100) * (sorted.length - 1);
        const lo = Math.floor(idx), hi = Math.ceil(idx);
        return sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo);
    },
    correlation(x, y) {
        const n = x.length;
        const mx = exports.math.mean(x), my = exports.math.mean(y);
        let num = 0, dx = 0, dy = 0;
        for (let i = 0; i < n; i++) {
            num += (x[i] - mx) * (y[i] - my);
            dx += (x[i] - mx) ** 2;
            dy += (y[i] - my) ** 2;
        }
        return num / Math.sqrt(dx * dy);
    },
    linearRegression(x, y) {
        const n = x.length;
        const mx = exports.math.mean(x), my = exports.math.mean(y);
        let num = 0, den = 0;
        for (let i = 0; i < n; i++) {
            num += (x[i] - mx) * (y[i] - my);
            den += (x[i] - mx) ** 2;
        }
        const slope = num / den;
        const intercept = my - slope * mx;
        const predicted = x.map(xi => slope * xi + intercept);
        const ssRes = y.reduce((s, yi, i) => s + (yi - predicted[i]) ** 2, 0);
        const ssTot = y.reduce((s, yi) => s + (yi - my) ** 2, 0);
        const r2 = 1 - ssRes / ssTot;
        return { slope, intercept, r2 };
    },
    /** Chi-squared statistic */
    chi2(observed, expected, errors) {
        let chi2 = 0;
        for (let i = 0; i < observed.length; i++) {
            chi2 += ((observed[i] - expected[i]) / errors[i]) ** 2;
        }
        return chi2;
    },
    /** Reduced chi-squared (chi²/dof) */
    reducedChi2(observed, expected, errors, nParams) {
        const dof = observed.length - nParams;
        return exports.math.chi2(observed, expected, errors) / dof;
    },
};
// ─── Live Data Fetchers (Public APIs, no keys) ───────────────────────────────
exports.live = {
    /** Fetch earthquake data (USGS, last 24h) */
    async earthquakes(minMagnitude = 4.5) {
        try {
            const url = `https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/${minMagnitude >= 4.5 ? '4.5' : '2.5'}_day.geojson`;
            const data = await fetchJSON(url);
            return data.features.map((f) => ({
                mag: f.properties.mag,
                place: f.properties.place,
                time: f.properties.time,
                lat: f.geometry.coordinates[1],
                lon: f.geometry.coordinates[0],
                depth: f.geometry.coordinates[2],
            }));
        }
        catch {
            return [];
        }
    },
    /** Fetch ISS position */
    async issPosition() {
        try {
            const data = await fetchJSON('http://api.open-notify.org/iss-now.json');
            return {
                lat: parseFloat(data.iss_position.latitude),
                lon: parseFloat(data.iss_position.longitude),
                altitude: 408, // approximate km
                velocity: 7.66, // km/s
            };
        }
        catch {
            return null;
        }
    },
    /** Fetch solar activity (NOAA) */
    async solarActivity() {
        try {
            const data = await fetchText('https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json');
            const parsed = JSON.parse(data);
            const latest = parsed[parsed.length - 1];
            return {
                sunspots: latest['ssn'] || 0,
                flux: latest['f10.7'] || 0,
                kp: 0, // would need separate endpoint
            };
        }
        catch {
            return null;
        }
    },
    /** Fetch latest arxiv papers (cosmology) */
    async arxivRecent(category = 'astro-ph.CO', maxResults = 5) {
        try {
            const url = `http://export.arxiv.org/api/query?search_query=cat:${category}&sortBy=submittedDate&sortOrder=descending&max_results=${maxResults}`;
            const xml = await fetchText(url);
            // Simple XML parsing (no dependency)
            const entries = [];
            const entryBlocks = xml.split('<entry>').slice(1);
            for (const block of entryBlocks) {
                const title = block.match(/<title>([\s\S]*?)<\/title>/)?.[1]?.trim() || '';
                const authors = block.match(/<name>(.*?)<\/name>/g)?.map(a => a.replace(/<\/?name>/g, '')).join(', ') || '';
                const summary = block.match(/<summary>([\s\S]*?)<\/summary>/)?.[1]?.trim().slice(0, 200) || '';
                const published = block.match(/<published>(.*?)<\/published>/)?.[1] || '';
                entries.push({ title, authors, summary, published });
            }
            return entries;
        }
        catch {
            return [];
        }
    },
};
//# sourceMappingURL=real-data.js.map