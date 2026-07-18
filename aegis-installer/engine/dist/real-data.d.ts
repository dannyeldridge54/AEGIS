/**
 * AEGIS — Real-World Data Connectors
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Live data feeds from real physical/financial/scientific sources.
 * Zero dependencies — uses Node's built-in http/https.
 */
export declare const physics: {
    /** NIST physical constants (2022 CODATA) */
    constants: {
        c: number;
        h: number;
        hbar: number;
        G: number;
        k_B: number;
        e: number;
        m_e: number;
        m_p: number;
        N_A: number;
        sigma: number;
        alpha: number;
        R_inf: number;
        mu_0: number;
        epsilon_0: number;
        H0_planck: number;
        H0_shoes: number;
        Omega_m: number;
        Omega_b: number;
        Omega_Lambda: number;
        T_cmb: number;
        t_universe: number;
        sigma_8: number;
        n_s: number;
    };
    /** Hubble rate measurements (z, H(z) km/s/Mpc, σ) — cosmic chronometers */
    hubbleData: {
        z: number;
        H: number;
        sigma: number;
    }[];
    /** BAO measurements (DESI DR1 2024 + SDSS) */
    baoData: ({
        z: number;
        DV_rd: number;
        sigma: number;
        source: string;
        DM_rd?: undefined;
        DH_rd?: undefined;
        DH_sigma?: undefined;
    } | {
        z: number;
        DM_rd: number;
        sigma: number;
        DH_rd: number;
        DH_sigma: number;
        source: string;
        DV_rd?: undefined;
    })[];
    /** Type Ia Supernovae (Pantheon+ binned, 20 bins) */
    sneData: {
        z: number;
        mu: number;
        sigma: number;
    }[];
    /** CMB acoustic scale and shift parameter (Planck 2018) */
    cmbData: {
        R_shift: {
            value: number;
            sigma: number;
        };
        l_A: {
            value: number;
            sigma: number;
        };
        omega_b: {
            value: number;
            sigma: number;
        };
        n_s: {
            value: number;
            sigma: number;
        };
        z_star: number;
        r_star: number;
        theta_star: number;
    };
    /** H₀ measurements from different methods */
    h0Measurements: {
        value: number;
        sigma: number;
        method: string;
        source: string;
    }[];
    /** Growth rate f·σ₈ measurements */
    growthData: {
        z: number;
        fsigma8: number;
        sigma: number;
    }[];
};
export declare const finance: {
    /** Fetch live stock/crypto price (no API key needed — uses free endpoints) */
    getPrice(symbol: string): Promise<{
        price: number;
        change: number;
        volume: number;
    } | null>;
    /** Common benchmark rates */
    rates: {
        fed_funds: number;
        us_10y: number;
        inflation_cpi: number;
        sp500_pe: number;
    };
};
export declare const environment: {
    /** Fetch current weather (Open-Meteo, no API key) */
    getWeather(lat: number, lon: number): Promise<{
        temperature: number;
        windSpeed: number;
        humidity: number;
        description: string;
    } | null>;
    /** Global climate data (key metrics) */
    climate: {
        co2_ppm_2024: number;
        global_temp_anomaly: number;
        sea_level_rise_mm_yr: number;
        arctic_ice_km2: number;
        ocean_ph: number;
    };
};
export declare const engineering: {
    /** Common material properties */
    materials: {
        steel_A36: {
            density: number;
            yield_MPa: number;
            E_GPa: number;
            poisson: number;
        };
        aluminum_6061: {
            density: number;
            yield_MPa: number;
            E_GPa: number;
            poisson: number;
        };
        titanium_Ti6Al4V: {
            density: number;
            yield_MPa: number;
            E_GPa: number;
            poisson: number;
        };
        concrete_C30: {
            density: number;
            compressive_MPa: number;
            E_GPa: number;
            poisson: number;
        };
        carbon_fiber: {
            density: number;
            tensile_MPa: number;
            E_GPa: number;
            poisson: number;
        };
        copper: {
            density: number;
            yield_MPa: number;
            E_GPa: number;
            conductivity_S_m: number;
        };
        glass: {
            density: number;
            tensile_MPa: number;
            E_GPa: number;
            poisson: number;
        };
    };
    /** Standard atmosphere (ISA) at altitude */
    atmosphere(altitude_m: number): {
        temperature_K: number;
        pressure_Pa: number;
        density_kg_m3: number;
    };
    /** Orbital mechanics */
    orbital: {
        earth_radius_km: number;
        earth_mass_kg: number;
        mu_earth: number;
        LEO_velocity_km_s: number;
        GEO_altitude_km: number;
        escape_velocity_km_s: number;
        /** Orbital velocity at given altitude */
        velocity(altitude_km: number): number;
        /** Orbital period at given altitude */
        period(altitude_km: number): number;
    };
};
export declare const math: {
    /** Standard statistical functions */
    mean(data: number[]): number;
    std(data: number[]): number;
    median(data: number[]): number;
    percentile(data: number[], p: number): number;
    correlation(x: number[], y: number[]): number;
    linearRegression(x: number[], y: number[]): {
        slope: number;
        intercept: number;
        r2: number;
    };
    /** Chi-squared statistic */
    chi2(observed: number[], expected: number[], errors: number[]): number;
    /** Reduced chi-squared (chi²/dof) */
    reducedChi2(observed: number[], expected: number[], errors: number[], nParams: number): number;
};
export declare const live: {
    /** Fetch earthquake data (USGS, last 24h) */
    earthquakes(minMagnitude?: number): Promise<Array<{
        mag: number;
        place: string;
        time: number;
        lat: number;
        lon: number;
        depth: number;
    }>>;
    /** Fetch ISS position */
    issPosition(): Promise<{
        lat: number;
        lon: number;
        altitude: number;
        velocity: number;
    } | null>;
    /** Fetch solar activity (NOAA) */
    solarActivity(): Promise<{
        sunspots: number;
        flux: number;
        kp: number;
    } | null>;
    /** Fetch latest arxiv papers (cosmology) */
    arxivRecent(category?: string, maxResults?: number): Promise<Array<{
        title: string;
        authors: string;
        summary: string;
        published: string;
    }>>;
};
//# sourceMappingURL=real-data.d.ts.map