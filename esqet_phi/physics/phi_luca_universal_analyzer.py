import numpy as np
from esqet_phi.constants import C_ALPHA_SCAR, LAMBDA_STERILE, PHI

class PhiLucaUniversalAnalyzer:
    """
    Universal analyzer that consumes observables from stand-alone instruments
    and returns a Φ_ESK coherence metric in [~ -1e-3, +1e-3] (dimensionless).
    """

    def __init__(self):
        self.phi_esk = 0.0

    # -------- Generic helpers --------
    def _field_evolution_step(self, S_current, dx=1e-3):
        laplacian = np.pad(
            (S_current[:-2] - 2*S_current[1:-1] + S_current[2:]) / dx**2,
            (1, 1)
        )
        grad_sq = np.pad(
            ((S_current[2:] - S_current[:-2]) / (2*dx))**2,
            (1, 1)
        )
        rhs = laplacian + C_ALPHA_SCAR * grad_sq + LAMBDA_STERILE * S_current
        return rhs

    # -------- Discipline-specific analyzers --------
    def analyze_lhc(self, jets_pt):
        grad_S = np.diff(np.sort(jets_pt))
        scar = C_ALPHA_SCAR * np.sum(grad_S**2)
        sterile = LAMBDA_STERILE * np.sum(jets_pt**2)
        self.phi_esk = scar - sterile
        return self.phi_esk

    def analyze_haystac(self, power_spectrum):
        # Use average excess power as proxy for coherence
        avg = np.mean(power_spectrum)
        self.phi_esk = C_ALPHA_SCAR * avg - 1e-3 * LAMBDA_STERILE
        return self.phi_esk

    def analyze_seti(self, waterfall_power):
        scar_pattern = C_ALPHA_SCAR * np.gradient(waterfall_power, axis=-1)**2
        self.phi_esk = float(np.mean(scar_pattern))
        return self.phi_esk

    def analyze_ligo(self, scalar_strain):
        signal = self._field_evolution_step(np.array(scalar_strain))
        self.phi_esk = float(np.mean(signal))
        return self.phi_esk

    def analyze_nasa_exoplanets(self, flux):
        # Coherence of periodic dips: variance of detrended flux
        flux = np.array(flux)
        detrended = flux - np.median(flux)
        scar = C_ALPHA_SCAR * float(np.var(detrended))
        self.phi_esk = scar - 1e-3 * LAMBDA_STERILE
        return self.phi_esk
