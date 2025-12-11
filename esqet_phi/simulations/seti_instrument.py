import numpy as np

def run_seti_observation(
    n_time: int = 256,
    n_freq: int = 1024,
    signal_snr: float = 15.0,
) -> dict:
    """
    Stand-alone SETI waterfall toy.
    Returns frequency axis, time axis, and waterfall power (2D).
    """
    time = np.linspace(0, 600.0, n_time)  # seconds
    freq = np.linspace(1.0, 2.0, n_freq)  # GHz

    waterfall = np.random.normal(0, 1.0, size=(n_time, n_freq))

    # Inject narrowband drifting signal
    f0_idx = int(0.3 * n_freq)
    drift_per_step = int(0.1 * n_freq / n_time)
    for t in range(n_time):
        idx = f0_idx + t * drift_per_step
        if 0 <= idx < n_freq:
            waterfall[t, idx] += signal_snr

    return {
        "time_s": time,
        "freq_ghz": freq,
        "waterfall_power": waterfall,
    }

if __name__ == "__main__":
    obs = run_seti_observation()
    print("SETI waterfall shape:", obs["waterfall_power"].shape)
