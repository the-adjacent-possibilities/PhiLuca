import numpy as np

def run_transit_photometry(
    mag: float = 11.0,
    duration_days: float = 27.0,
    cadence_min: float = 2.0,
    period_days: float = 5.0,
    radius_ratio: float = 0.1,
    noise_ppm: float = 200.0,
) -> dict:
    """
    Kepler/TESS-like light curve generator.
    Returns time (days) and relative flux with transits + noise.
    """
    t = np.arange(0, duration_days, cadence_min/1440.0)
    flux = np.ones_like(t)

    depth = radius_ratio**2
    phase = (t % period_days) / period_days
    in_transit = (phase > 0.49) & (phase < 0.51)
    flux[in_transit] -= depth

    sigma = noise_ppm * 1e-6
    flux += np.random.normal(0, sigma, size=flux.shape)

    return {"time_days": t, "flux": flux}

if __name__ == "__main__":
    obs = run_transit_photometry()
    print("NASA light-curve points:", len(obs["time_days"]))
