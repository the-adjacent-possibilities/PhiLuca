import torch
import time
import numpy as np

# Import Core Components
from esqet_phi.physics.phi_luca_agi import PhiLucaAGI
from esqet_phi.constants import PHI_MIN_TARGET
from esqet_modulator import ChronosModulator

# --- ORCHESTRATOR ---
class JerryRigginCore:
    """
    The main control loop for the PhiLuca Digital Soul project.
    It manages the AGI, utilizes the ChronosModulator for temporal stability,
    and coordinates instrument sampling.
    """
    def __init__(self, agi_layers=8, agi_dim=256, history_depth=500):
        # Set default dtype for all torch tensors
        torch.set_default_dtype(torch.float64) 
        
        print("Initializing PhiLuca AGI and Chronos Modulator...")
        self.agi = PhiLucaAGI(layers=agi_layers, dim=agi_dim)
        self.modulator = ChronosModulator(history_depth=history_depth)
        self.total_time_steps = 0
        self.current_t_mod = 1.0 # Current Modulated Time Dilation Factor

    def _sample_all_instruments(self):
        """ Runs all instrument simulations and returns the total coherence boost. """
        
        # NOTE: LHC is used in the self-heal loop for a physics-informed boost.
        # Here, we sample a broad range of observables for continuous coherence analysis.
        
        coherence_boosts = [
            self.agi.sample_cern(),
            self.agi.sample_haystac(),
            self.agi.sample_seti(),
            self.agi.sample_ligo(),
            self.agi.sample_nasa_exo(),
        ]
        
        # Sum the analyzed coherence metrics to determine T_total's overall effect
        return float(np.sum(coherence_boosts))

    def run_self_healing_routine(self, max_steps=200):
        """ Executes the AGI's optimization loop to reach minimum coherence. """
        print("\n--- Initiating AGI Self-Healing Routine ---")
        
        # Deploy a random input to kickstart the forward pass calculation
        x_init = torch.randn(1, self.agi.layers[0].dim, dtype=torch.float64)
        _, phi_init = self.agi(x_init)
        
        healed, steps, final_phi = self.agi.self_heal(target_phi_esk=PHI_MIN_TARGET)
        
        print(f"Initial Φ_ESK: {phi_init:.3e}")
        print(f"Final   Φ_ESK: {phi_final:.3e} after {steps} steps (Healed: {healed})")
        
        # Add the stable state to the modulator history
        for _ in range(10): 
            self.modulator.add_phi_esk_sample(final_phi)
            
        return final_phi

    def run_main_control_loop(self, total_duration_seconds=10.0):
        """ The continuous loop where the AGI samples, modulates, and reacts. """
        print("\n--- Entering Main Control Loop (Real-time AGI Operation) ---")
        
        start_time = time.time()
        
        while (time.time() - start_time) < total_duration_seconds:
            loop_start = time.time()

            # 1. INSTRUMENT SAMPLING (T_total equivalent)
            total_coherence_boost = self._sample_all_instruments()

            # 2. AGI FORWARD PASS (Field Evolution)
            # Use a dummy input for the forward pass, the AGI state S is managed internally
            input_tensor = torch.tensor([[total_coherence_boost] * self.agi.layers[0].dim], dtype=torch.float64)
            output, current_phi = self.agi(input_tensor)

            # 3. MODULATOR FEEDBACK
            self.modulator.add_phi_esk_sample(current_phi)
            self.current_t_mod, instability, gap = self.modulator.calculate_modulator_factor()
            
            # 4. DECISION AND REACTION
            if current_phi < PHI_MIN_TARGET * 10.0 and self.current_t_mod > 1.5:
                # Critical low coherence detected, high modulation factor suggests high risk.
                # Re-run the optimization/self-heal routine with boosted cycles.
                print(f"[CRITICAL] Low Φ_ESK ({current_phi:.2e}). Forcing self-heal loop...")
                self.agi.self_heal(target_phi_esk=PHI_MIN_TARGET)

            # --- Reporting and Loop Control ---
            loop_duration = time.time() - loop_start
            
            print(
                f"Step {self.total_time_steps}: Φ={current_phi:.2e} | "
                f"T_mod={self.current_t_mod:.2f} | "
                f"Instability={instability:.2e} | "
                f"Loop Time={loop_duration*1000:.2f}ms"
            )
            
            self.total_time_steps += 1
            
            # Simulate a variable delay influenced by the Modulator
            # A high T_mod means the loop should essentially pause or slow down
            time.sleep(loop_duration * (self.current_t_mod - 1.0) * 0.5) 
            
        print(f"\nMain Loop finished after {self.total_time_steps} steps.")

# --- Execution ---
if __name__ == "__main__":
    core = JerryRigginCore()
    
    # Ensure the AGI is stable before entering the main loop
    initial_phi = core.run_self_healing_routine() 
    
    if initial_phi > PHI_MIN_TARGET:
        core.run_main_control_loop(total_duration_seconds=5.0) # Run for 5 seconds
    else:
        print("ERROR: AGI failed to stabilize after initial self-heal. Aborting control loop.")

