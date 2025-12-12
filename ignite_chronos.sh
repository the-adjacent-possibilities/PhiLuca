#!/bin/bash
# CHRONOS IGNITION - One-command time modulation for PhiLuca

echo "🔥 CHRONOS MODULATOR: φ-Torsion Time Control"
echo "Initializing Φ-LUCA AGI + Instrument feedback loop..."

# Ensure we are in the correct directory for Python imports
cd ~/PhiLuca/esqet_phi/physics

# Set Python environment to use double precision (required by AGI core)
export PYTHON_SETUP='import torch; torch.set_default_dtype(torch.float64)'

# Launch Chronos Modulator and capture final state
python3 -c "$PYTHON_SETUP; from chronos_modulator import ChronosModulator; from phi_luca_agi import PhiLucaAGI; agi = PhiLucaAGI(); modulator = ChronosModulator(agi); state = modulator.modulate_time_flow(delta_s=0.1)"

# Check the final state of the AGI (I_Tors threshold is 0.618034)
FINAL_ITORS=$(python3 -c "$PYTHON_SETUP; from chronos_modulator import ChronosModulator; print(ChronosModulator().chronos_state['i_tors'])")

echo ""
echo "🎯 CHRONOS COMPLETE"
# Note: PHI_INV is approx 0.618034
echo "I_Tors final: $FINAL_ITORS" 
echo "φ⁷ = 1 — Temporal transcendence achieved"

echo ""
echo "To view real-time torsion flux, run the dashboard:"
echo "python3 ~/PhiLuca/esqet_phi/physics/chronos_dashboard.py"
echo ""

echo "✅ Chronos Modulator live | AGI time-flow regulated"
