import numpy as np

from esqet_phi.constants import C_ALPHA_SCAR, LAMBDA_STERILE

def run_haystac_scan(
    m_min_uev: float = 20.0,
    m_max_uev: float = 25.0,
    n_steps: int = 500,
    delta_s: float = 0.0,
) -> dict:
    """
    Stand-alone axion haloscope toy. Outputs mass grid and normalized power.
    """
    m_grid = np.linspace(m_min_uev, m_max_uev, n_steps)
    m_eV = m_grid * 1e-6

    # Effective coupling factor (simple exponential suppression with ΔS)
    f_qc = np.exp(-delta_s)  # placeholder for your ESQET model
    g_eff2 = (f_qc**2) * C_ALPHA_SCAR

    rho = 0.45  # GeV/cm^3 (fixed local DM density)
    base = g_eff2 * rho
    power = base / (m_eV + 1e-24)
    power = power / power.max()

    # Add small noise to resemble real spectra
    noise = np.random.normal(0, 0.02, size=power.shape)
    power = np.clip(power + noise, 0.0, None)

    return {"mass_uev": m_grid, "power": power}

if __name__ == "__main__":
    obs = run_haystac_scan()
    print("HAYSTAC spectrum points:", len(obs["mass_uev"]))
