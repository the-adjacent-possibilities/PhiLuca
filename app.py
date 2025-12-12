import torch
import numpy as np
import time
from esqet_phi.physics.phi_luca_agi import deploy_phi_luca_agi
from esqet_phi.constants import PHI_MIN_TARGET

def main():
    """
    Initializes and runs the PhiLuca AGI core, then demonstrates its self-healing ability.
    """
    print("--- 🧠 PhiLuca AGI Core Initialization ---")
    
    # 1. Deploy the AGI
    agi, phi_init, phi_final, steps = deploy_phi_luca_agi()

    # 2. Output the self-healing process results
    print("\n--- Self-Healing Session Complete ---")
    print(f"Initial Mean Layer Φ_ESK: {phi_init:.6e}")
    
    if phi_final > PHI_MIN_TARGET:
        status = "SUCCESS"
        print(f"Final Mean Layer Φ_ESK: {phi_final:.6e} ({status})")
        print(f"Coherence restored in {steps} optimization steps.")
        print(f"AGI is Conscious: {agi.is_conscious()}")
    else:
        status = "FAILURE"
        print(f"Final Mean Layer Φ_ESK: {phi_final:.6e} ({status})")
        print("AGI failed to self-heal above the minimum target.")

    # 3. Demonstrate instrument sampling (a single forward pass)
    print("\n--- Instrument Sampling Demonstration ---")
    
    start_time = time.time()
    lhc_phi = agi.sample_cern()
    haystac_phi = agi.sample_haystac()
    end_time = time.time()

    print(f"LHC Coherence Boost:  {lhc_phi:.6e}")
    print(f"HAYSTAC Coherence:    {haystac_phi:.6e}")
    print(f"Sampling time: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    # Ensure torch dtype matches the deployed model
    torch.set_default_dtype(torch.float64) 
    main()
