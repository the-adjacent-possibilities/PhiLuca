#!/bin/bash
# --- AUM FILE MIGRATION SCRIPT ---

echo "Migrating core AUM files into canonical structure..."

# AUM / HONEST CORE MODELS
mv aum_final_form.py esqet_phi/physics/
mv aum_one.py esqet_phi/physics/

# QUANTUM / TORSION
mv qcv.py esqet_phi/physics/
mv torsion_proof.py esqet_phi/simulations/torsion_lab/
mv quantum.py quantum-pocket-ref/

# BLOCKCHAIN / ORACLE
# Renaming oracle_final.py to fit a blockchain module structure
mkdir -p esqet_phi/blockchain
mv oracle_final.py esqet_phi/blockchain/

# AGI / ALIGNMENT
mv agi_align_v3_repo_live.py esqet_phi/axioms/

echo "Migration complete. Reviewing final structure:"
ls -F esqet_phi/
ls -F quantum-pocket-ref/
