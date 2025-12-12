import os
import json
import requests
from typing import Dict, List

# --- ESQET CONSTANTS ---
PHI_INV = 0.61803398 # Torsion Incoherence Limit
PHI = 1.61803398 # Maximum Coherence
BASE_COH_STATUS = 1.0

# --- ANSI Color Constants ---
ANSI_BLUE = "\033[94m"
ANSI_GREEN = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_RED = "\033[91m"
ANSI_RESET = "\033[0m"

# --- Constants for Config Paths ---
HOME_DIR = os.path.expanduser("~")
# Assuming the user fixed the .env path issue based on prior context:
ENV_PATH = os.path.join(HOME_DIR, "PhiLuca", ".env") 
APIKEY_PATH = os.path.join(HOME_DIR, "storage", "downloads", "apikey.json")
CREDENTIALS_PATH = os.path.join(HOME_DIR, "storage", "downloads", "credentials.json")

# Auto-Install & Import dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    print(f"{ANSI_RED}[FATAL] Missing python-dotenv. Please run 'pip install python-dotenv --user'{ANSI_RESET}")
    exit(1)

# Auto-Install & Import requests
try:
    import requests
except ImportError:
    print(f"{ANSI_CYAN}[INFO] Installing requests library...{ANSI_RESET}")
    os.system("pip install requests --user")
    import requests

# Load .env
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)
    print(f"{ANSI_GREEN}✅ LOADED: Environmental Axiom (.env) loaded from {ENV_PATH}{ANSI_RESET}")
else:
    print(f"{ANSI_RED}❌ ERROR: .env not found at {ENV_PATH}. Cannot proceed with Functional Coherence Check.{ANSI_RESET}")
    exit(1)

# Expected Vars
expected_vars = [
    "GROQ_API_KEY", "IBM_TOKEN", "PINATA_JWT", "ETHERSCAN_IO_API_KEY", 
    "NASA_API_KEY", "USGS_API", "EXPO_TOKEN", 
    # Non-API vars (checked syntactically only)
    "GIT_USER_NAME", "PRIVATE_KEY", "PHICOIN_WALLET", "DEBUG_MODE"
]

# --- 1. FUNCTIONAL COHERENCE TEST SUITE (G-COH) ---

def test_api_functional_coherence(key_name: str, endpoint: str, headers: Dict[str, str] = None, method: str = 'GET') -> float:
    """Tests if an API key/token is functional and yields G-COH status."""
    key = os.getenv(key_name)
    if not key:
        return 0.0 # NULL Coherence (Missing)

    try:
        # For keys in headers, use the provided headers or construct a default
        if headers is None:
            if 'GROQ' in key_name or 'IBM' in key_name:
                headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            else:
                # If key is embedded (like NASA/Etherscan), assume simple request and key is in the endpoint
                pass
        
        timeout = 5
        response = requests.request(method, endpoint, headers=headers, timeout=timeout)
        
        # 200/204/400 (if message indicates success/key recognized) means Functional Coherence
        if response.status_code in [200, 204]:
            return BASE_COH_STATUS # 1.0 (Full Coherence)
        
        # Specific check for API errors where the key is clearly rejected (e.g., 401)
        if response.status_code in [401, 403]:
            return PHI_INV # 0.618 (Torsion Incoherence: Key Rejected)
        
        # Any other failure (404, 500) might be endpoint issues, not key, so treat as warning
        return PHI_INV # Treat as temporary incoherence

    except requests.exceptions.Timeout:
        return PHI_INV # 0.618 (Temporal Dilation Incoherence)
    except Exception as e:
        return PHI_INV # 0.618 (Internal System Error/Generic Incoherence)

# --- Define Specific Tests using the Generic Function ---

def run_all_tests() -> Dict[str, float]:
    """Runs all functional and syntactic tests."""
    functional_results = {}

    print(f"\n{ANSI_BLUE}--- INITIATING FUNCTIONAL COHERENCE (G-COH) TESTS ---{ANSI_RESET}")

    # 1. GROQ (LLM Core) - Requires Authorization header
    functional_results["GROQ_API_KEY"] = test_api_functional_coherence(
        "GROQ_API_KEY", 
        "https://api.groq.com/openai/v1/models",
        method='GET'
    )
    
    # 2. IBM QUANTUM - Requires Authorization header (simple listing test)
    functional_results["IBM_TOKEN"] = test_api_functional_coherence(
        "IBM_TOKEN", 
        "https://api-qcon.quantum-computing.ibm.com/api/Hubs/q-research/Groups/internal/Projects/research/devices",
        method='GET'
    )
    
    # 3. NASA (Data Inflow) - Key is typically a query parameter
    functional_results["NASA_API_KEY"] = test_api_functional_coherence(
        "NASA_API_KEY", 
        f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('NASA_API_KEY')}",
        method='GET'
    )

    # 4. ETHERSCAN (Web3/Blockstream) - Key is typically a query parameter
    functional_results["ETHERSCAN_IO_API_KEY"] = test_api_functional_coherence(
        "ETHERSCAN_IO_API_KEY", 
        f"https://api.etherscan.io/api?module=stats&action=ethprice&apikey={os.getenv('ETHERSCAN_IO_API_KEY')}",
        method='GET'
    )

    # 5. PINATA (IPFS/Immutability) - Uses JWT
    pinata_jwt = os.getenv("PINATA_JWT")
    if pinata_jwt:
        functional_results["PINATA_JWT"] = test_api_functional_coherence(
            "PINATA_JWT", 
            "https://api.pinata.cloud/data/testAuthentication",
            headers={"Authorization": f"Bearer {pinata_jwt}"}
        )
    else:
        functional_results["PINATA_JWT"] = 0.0

    # 6. EXPO (Mobile/Dashboard Build) - Requires Authorization header
    functional_results["EXPO_TOKEN"] = test_api_functional_coherence(
        "EXPO_TOKEN", 
        "https://api.expo.dev/v2/users/@me",
        method='GET'
    )

    print(f"{ANSI_BLUE}--- FUNCTIONAL COHERENCE TESTS COMPLETE ---{ANSI_RESET}")

    # --- 2. SYNTACTIC COHERENCE CHECK (Fallback for non-API keys) ---
    syntactic_results = {}
    for var in expected_vars:
        if var not in functional_results:
            value = os.getenv(var)
            if value:
                syntactic_results[var] = BASE_COH_STATUS # 1.0 (Syntactic Coherence)
            else:
                syntactic_results[var] = 0.0 # 0.0 (NULL Coherence)

    functional_results.update(syntactic_results)
    return functional_results

# --- 3. DISPLAY AND REPORT ---

def report_coherence(results: Dict[str, float]):
    """Displays the final G-COH status for all variables."""
    print(f"\n{ANSI_BLUE}--- ESQET TORSION FIELD COHERENCE REPORT (G-COH) ---{ANSI_RESET}")
    print(f"{ANSI_GREEN}G-COH (1.000): Full Coherence (API Active){ANSI_RESET}")
    print(f"{ANSI_YELLOW}T-INCOH (0.618): Torsion Incoherence (API Rejected/Failure){ANSI_RESET}")
    print(f"{ANSI_RED}NULL (0.000): Variable Missing (Field Collapse){ANSI_RESET}")
    print(f"-------------------------------------------------------")

    total_coherence = 0
    total_vars = len(results)

    for key, coh in results.items():
        color = ANSI_GREEN
        status = "G-COH"
        if coh == 0.0:
            color = ANSI_RED
            status = "NULL"
        elif coh < 1.0:
            color = ANSI_YELLOW
            status = "T-INCOH"
        
        print(f"| {key:<25} | {color}{status:<8} ({coh:.3f}){ANSI_RESET}")
        total_coherence += coh
    
    # Calculate Mean G-COH (The overall stability metric)
    mean_g_coh = total_coherence / total_vars if total_vars > 0 else 0.0

    print(f"-------------------------------------------------------")
    color = ANSI_GREEN if mean_g_coh >= 0.9 else (ANSI_YELLOW if mean_g_coh >= PHI_INV else ANSI_RED)
    
    print(f"{ANSI_BLUE}TOTAL SYSTEM MEAN G-COH: {color}{mean_g_coh:.4f}{ANSI_RESET}")
    
    if mean_g_coh < PHI_INV:
        print(f"{ANSI_RED}SYSTEM WARNING: BELOW TORSION INCOHERENCE LIMIT (0.618). CRITICAL DATA STREAMS ARE COLLAPSED.{ANSI_RESET}")
    elif mean_g_coh < 0.9:
        print(f"{ANSI_YELLOW}SYSTEM WARNING: INCOHERENCE DETECTED. SOME DATA STREAMS ARE REJECTED. CHECK T-INCOH KEYS.{ANSI_RESET}")
    else:
        print(f"{ANSI_GREEN}SYSTEM STABLE: ALL EXTERNAL DATA STREAMS ARE FUNCTIONALLY COHERENT.{ANSI_RESET}")


# --- EXECUTION ---
if __name__ == "__main__":
    coherence_results = run_all_tests()
    report_coherence(coherence_results)


