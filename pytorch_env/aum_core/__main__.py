from aum_core.chronos.esqet_modulator import chronos
from aum_core.axioms.jerry_riggin_core import JRA
import time

print("\nAUM — WELCOME-TO-THE-GOD\n")
print("Atomic Chronos Modulator ACTIVE")
print(f"ϕ⁻¹ threshold: {JRA.PHI_INV:.12f}")
print(f"Initial I_Tors: {JRA.torsion_index:.12f}\n")

while True:
    chronos.enforce_coherence()
    time.sleep(0.618033988749)  # One ϕ-second heartbeat
