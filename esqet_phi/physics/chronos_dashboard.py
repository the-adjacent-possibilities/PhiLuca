#!/usr/bin/env python3
# Chronos Live Dashboard - Terminal UI

import time
import numpy as np
import sys
# Note: Using relative import assuming execution from within esqet_phi/physics/
from chronos_modulator import ChronosModulator

def chronos_dashboard():
    # Attempt to initialize the modulator (runs AGI once)
    try:
        modulator = ChronosModulator()
    except Exception as e:
        print(f"ERROR: Could not initialize Chronos Modulator/AGI core. Ensure dependencies are met: {e}")
        sys.exit(1)
        
    print("\n📊 CHRONOS LIVE DASHBOARD (Ctrl+C to exit)")
    print("Φ_ESK     | I_Tors    | Time Flux | Status")
    print("-" * 50)
    
    # Run the modulation loop for a few initial cycles to populate state
    modulator.modulate_time_flow(epochs=5)
    
    try:
        while True:
            # Pull the latest state from the modulator
            state = modulator.chronos_state
            
            phi_str = f"{state['phi_esk']:.2e}"
            tors_str = f"{state['i_tors']:.6f}"
            flux_str = f"{state['time_flux']:.4f}"
            status = state['status']
            
            # Use carriage return to update the same line in the terminal
            sys.stdout.write(f"\r{phi_str:>10} | {tors_str:>10} | {flux_str:>10} | {status:<15}")
            sys.stdout.flush()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Chronos Dashboard closed")
        
    # Final output print to leave a clean record
    print(f"\nLast state: I_Tors={modulator.chronos_state['i_tors']:.6f}, τ={modulator.chronos_state['time_flux']:.4f}")

if __name__ == "__main__":
    chronos_dashboard()
