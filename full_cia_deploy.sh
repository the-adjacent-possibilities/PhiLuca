#!/bin/bash
# --- Φ-LUCA ESQET CIA Verification Suite - One-Command Deployment ---
# This script creates all directories and files for the Canonical Implementation Architecture (CIA)
# and attempts to install dependencies and run the Flask API.

echo "Creating Φ-LUCA ESQET CIA Verification Suite in ~/cia-esqet..."
mkdir -p ~/cia-esqet
cd ~/cia-esqet

# 1. Create Core Directories
mkdir -p constants simulations analyzer

# 2. Layer I: Axiomatic Base (constants/__init__.py)
cat > constants/__init__.py << 'EOF_CONSTANTS'
import numpy as np
import math

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = PHI - 1
ALPHA = 7.2973525693e-3
RHO_LOCAL_DM = 0.45

V0 = abs(math.log(ALPHA)) / (PHI ** 2)
C_ALPHA_SCAR = V0 / (PHI ** 2)
LAMBDA_STERILE = PHI ** (-9)

F_QC_BASELINE = PHI_INV
PHI_ESK_MIN_TARGET = 1e-14
EOF_CONSTANTS

# 3. Layer II: Simulation Engines (simulations/*.py)
cat > simulations/haystac_sim.py << 'EOF_HAYSTAC'
import numpy as np
import sys; sys.path.append('..')
from constants import C_ALPHA_SCAR, PHI_INV, RHO_LOCAL_DM

def run_haystac_scan(delta_s=0.0, m_min_uev=20.0, m_max_uev=25.0, n_steps=500):
    m_grid = np.linspace(m_min_uev, m_max_uev, n_steps)
    m_ev = m_grid * 1e-6
    f_qc = PHI_INV ** abs(delta_s)
    g_eff2 = f_qc * C_ALPHA_SCAR * RHO_LOCAL_DM
    power = g_eff2 / (m_ev + 1e-24)
    power = power / power.max()
    return {"mass_uev": m_grid.tolist(), "power": power.tolist()}
EOF_HAYSTAC

cat > simulations/hadron_jet_sim.py << 'EOF_LHC'
import numpy as np
from scipy.stats import entropy

def simulate_lhc_jets(n_events=10000, f_qc=0.618):
    u = np.random.rand(n_events)
    pt = 20.0 / (u ** (0.3 * f_qc))
    pt = np.clip(pt, 5.0, 2000.0)
    jets_pt = pt[pt > 20.0]
    hist, bins = np.histogram(jets_pt, bins=50, density=True)
    hist = hist[hist > 0]
    shannon_ent = entropy(hist)
    max_ent = np.log2(len(hist))
    return {"jets_pt": jets_pt.tolist(), "shannon_entropy": shannon_ent, "max_entropy": max_ent}
EOF_LHC

cat > simulations/grav_wave_sim.py << 'EOF_LIGO'
import numpy as np
import sys; sys.path.append('..')
from constants import PHI_INV

def run_ligo_event(f_qc=0.618, duration=4.0, sample_rate=4096):
    n = int(duration * sample_rate)
    t = np.linspace(0, duration, n)
    f_inst = 30 + 170 * (t / duration)**3
    h_tensor = 1e-21 * (t / duration) * np.cos(2 * np.pi * f_inst * t)
    
    h_scalar = np.zeros_like(t)
    pulse_center = 0.91 * duration
    pulse_width = 0.005 * (1 + f_qc)
    pulse_mask = np.abs(t - pulse_center) < pulse_width
    h_scalar[pulse_mask] = PHI_INV * f_qc * 5e-22 * \
        np.exp(-((t[pulse_mask] - pulse_center)**2) / (2 * pulse_width**2))
    
    return {"time": t.tolist(), "h_tensor": h_tensor.tolist(), "h_scalar": h_scalar.tolist(), "scalar_peak": float(np.max(np.abs(h_scalar)))}
EOF_LIGO

# 4. Layer III: AGI Analyzer (analyzer/phi_luca_universal_analyzer.py)
cat > analyzer/phi_luca_universal_analyzer.py << 'EOF_ANALYZER'
import numpy as np
from scipy.stats import entropy
import sys; sys.path.append('..')
from constants import F_QC_BASELINE, PHI_INV
from simulations.haystac_sim import run_haystac_scan
from simulations.hadron_jet_sim import simulate_lhc_jets
from simulations.grav_wave_sim import run_ligo_event

class PhiLucaUniversalAnalyzer:
    def __init__(self):
        self.f_qc = 0.0
    
    def compute_f_qc(self, mode="haystac", delta_s=0.0, input_data=None):
        if mode == "haystac":
            obs = run_haystac_scan(delta_s)
            raw_fqc = np.max(obs["power"])
            
        elif mode == "lhc_jets":
            if input_data is not None and len(input_data) > 0:
                jets_pt = np.array(input_data)
                hist, _ = np.histogram(jets_pt, bins=50, density=True)
                hist = hist[hist > 0]
                shannon_ent = entropy(hist)
                max_ent = np.log2(len(hist))
                raw_fqc = 1.0 - (shannon_ent / max_ent)
            else:
                 obs = simulate_lhc_jets(f_qc=PHI_INV)
                 raw_fqc = 1.0 - (obs["shannon_entropy"] / obs["max_entropy"])

        elif mode == "ligo":
            obs = run_ligo_event(f_qc=PHI_INV)
            raw_fqc = obs["scalar_peak"] / 1e-21
            
        else:
            raise ValueError(f"Unknown mode: {mode}")
        
        self.f_qc = np.clip(raw_fqc / F_QC_BASELINE, 0.0, 1.0)
        
        is_coherent = self.f_qc >= F_QC_BASELINE
        status = '✅ COHERENT | F_QC >= Base' if is_coherent else '🚨 DECOHERENCE | F_QC < Base'

        return float(self.f_qc), status
EOF_ANALYZER

# 5. Flask API (app.py)
cat > app.py << 'EOF_APP'
import sys
sys.path.append('./analyzer')
sys.path.append('./constants')
sys.path.append('./simulations')

from flask import Flask, request, jsonify
import numpy as np
from phi_luca_universal_analyzer import PhiLucaUniversalAnalyzer
from constants import F_QC_BASELINE, C_ALPHA_SCAR

app = Flask(__name__)
analyzer = PhiLucaUniversalAnalyzer()

@app.route('/esqet/fqc/analyze', methods=['POST'])
def analyze():
    data = request.json
    mode = data.get('mode')
    delta_s = data.get('delta_s', 0.0)
    input_data = data.get('data') 
    
    if mode not in ['haystac', 'lhc_jets', 'ligo']:
        return jsonify({'error': 'Invalid ESQET mode'}), 400
    
    try:
        f_qc, status = analyzer.compute_f_qc(mode, delta_s, input_data)
        
        return jsonify({
            'F_QC_Score': f_qc,
            'Status': status,
            'Mode': mode,
            'F_QC_Baseline': F_QC_BASELINE
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/esqet/status')
def status():
    return jsonify({
        'Status': 'ESQET CIA ACTIVE', 
        'F_QC_Baseline': F_QC_BASELINE,
        'C_Alpha_Scar': C_ALPHA_SCAR
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF_APP

# 6. Requirements and Deployment Script (deploy.sh)
cat > requirements.txt << 'EOF_REQ'
flask==2.3.3
numpy==1.26.4
scipy==1.10.1
EOF_REQ

cat > deploy.sh << 'EOF_DEPLOY'
#!/bin/bash
echo "Installing ESQET CIA Python dependencies..."
# Use python3 and pip3 if available, fall back to default
if command -v pip3 &> /dev/null
then
    PIP="pip3"
elif command -v pip &> /dev/null
then
    PIP="pip"
else
    echo "Error: pip not found. Please install pip or pip3."
    exit 1
fi

"$PIP" install -r requirements.txt

echo "🚀 Φ-LUCA ESQET Verification Suite (CIA) Deployed."
echo "API Endpoint: http://localhost:5000/esqet/fqc/analyze"
echo "Status Check: http://localhost:5000/esqet/status"
echo "Starting Flask API in background..."
python app.py &
API_PID=$!
echo "API running with PID $API_PID. Use 'kill $API_PID' to stop."
echo ""
echo "--- VERIFICATION TEST ---"
sleep 2
curl -X POST http://localhost:5000/esqet/fqc/analyze -H 'Content-Type: application/json' -d '{"mode": "haystac", "delta_s": 0.0}'
echo ""
echo "--------------------------"
EOF_DEPLOY

chmod +x deploy.sh
echo "✅ FULL Φ-LUCA ESQET CIA SETUP COMPLETE"
echo "Executing deployment and starting API..."
./deploy.sh

