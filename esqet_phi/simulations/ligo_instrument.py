import numpy as np

def run_ligo_event(
    mass_1: float = 30.0,
    mass_2: float = 30.0,
    duration: float = 4.0,
    sample_rate: int = 4096,
    noise_level: float = 1e-21,
) -> dict:
    """
    Stand-alone LIGO toy: inspiral+ringdown + Gaussian noise.
    Returns time, tensor strain, and scalar channel.
    """
    n = int(duration * sample_rate)
    t = np.linspace(0, duration, n, endpoint=False)

    # Crude chirp model
    f0 = 30.0
    f1 = 200.0
    f_inst = f0 + (f1 - f0) * (t / duration)**3
    amp = 1e-21 * (t / duration)
    h_tensor = amp * np.cos(2 * np.pi * f_inst * t)

    # Ringdown tail
    ring_mask = t > 0.8 * duration
    tau = 0.1
    h_tensor[ring_mask] += 5e-22 * np.exp(-(t[ring_mask] - 0.8*duration) / tau) * \
        np.cos(2 * np.pi * f1 * (t[ring_mask] - 0.8*duration))

    # Optional scalar pulse (non-oscillatory burst)
    h_scalar = np.zeros_like(t)
    pulse_mask = (t > 0.9 * duration) & (t < 0.92 * duration)
    h_scalar[pulse_mask] = 5e-22 * np.exp(-((t[pulse_mask] - 0.91*duration)**2) / (2*(0.005**2)))

    noise = np.random.normal(0, noise_level, size=n)
    return {"time": t, "h_tensor": h_tensor + noise, "h_scalar": h_scalar}

if __name__ == "__main__":
    obs = run_ligo_event()
    print("LIGO strain length:", len(obs["time"]))
