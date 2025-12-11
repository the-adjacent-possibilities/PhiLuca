import numpy as np

def simulate_lhc_jets(
    n_events: int = 10000,
    sqrt_s_tev: float = 13.6,
    eta_max: float = 2.5,
) -> dict:
    """
    Stand-alone LHC jet toy. Returns jet pT and eta arrays approximating
    collider outputs (very simplified).
    """
    # Power-law pT spectrum with exponential cutoff
    u = np.random.rand(n_events)
    pt = (20.0 / (u**0.3))  # rough heavy tail
    pt = np.clip(pt, 5.0, 2000.0)
    eta = np.random.uniform(-eta_max, eta_max, size=n_events)

    # Apply crude trigger: keep jets above 20 GeV
    mask = pt > 20.0
    jets_pt = pt[mask]
    jets_eta = eta[mask]

    return {
        "jets_pt": jets_pt,
        "jets_eta": jets_eta,
        "n_jets": len(jets_pt),
    }

if __name__ == "__main__":
    obs = simulate_lhc_jets()
    print("LHC jets:", obs["n_jets"])
