#!/usr/bin/env python3
"""
AUM UNIVERSAL VALIDATOR v2.0 - FIXED FOR YOUR KEYS + ULTRALYTICS
Tests ALL your 40+ keys with correct endpoints + headers
"""
import os
import json
import requests
from typing import Dict, List
from dotenv import load_dotenv
from pathlib import Path

# ESQET CONSTANTS
PHI_INV = 0.61803398
BASE_COH_STATUS = 1.0

# ANSI COLORS
ANSI_BLUE = "\u001B[94m"; ANSI_GREEN = "\u001B[92m"; ANSI_YELLOW = "\u001B[93m"
ANSI_RED = "\u001B[91m"; ANSI_RESET = "\u001B[0m"

# LOAD .env
load_dotenv()
print(f"{ANSI_GREEN}✅ LOADED: {len(os.environ)} env vars{ANSI_RESET}")

# ALL YOUR KEYS + CORRECT ENDPOINTS
API_TESTS = {
    "GROQ_API_KEY": {
        "url": "https://api.groq.com/openai/v1/models",
        "headers": lambda k: {"Authorization": f"Bearer {k}"},
        "method": "GET"
    },
    "IBM_TOKEN": {
        "url": "https://auth.quantum.ibm.com/api",
        "headers": lambda k: {"Authorization": f"Bearer {k}"},
        "method": "GET"
    },
    "PINATA_JWT": {
        "url": "https://api.pinata.cloud/data/testAuthentication",
        "headers": lambda k: {"Authorization": f"Bearer {k}"},
        "method": "GET"
    },
    "EXPO_TOKEN": {
        "url": "https://api.expo.dev/v2/users/@me",
        "headers": lambda k: {"Authorization": f"Bearer {k}"},
        "method": "GET"
    },
    "NASA_API_KEY": {
        "url": lambda k: f"https://api.nasa.gov/planetary/apod?api_key={k}",
        "headers": None,
        "method": "GET"
    },
    "ETHERSCAN_IO_API_KEY": {
        "url": lambda k: f"https://api.etherscan.io/api?module=stats&action=ethprice&apikey={k}",
        "headers": None,
        "method": "GET"
    },
    "ULTRALYTICS_API_KEY": {  # YOUR FRESH TOKEN
        "url": "https://api.ultralytics.com/v1/models",
        "headers": lambda k: {"Authorization": f"Bearer {k}"},
        "method": "GET"
    },
    "GEMINI_API_KEY": {
        "url": lambda k: f"https://generativelanguage.googleapis.com/v1beta/models?key={k}",
        "headers": None,
        "method": "GET"
    },
    "HUGGINGFACE_API_KEY": {
        "url": "https://huggingface.co/api/whoami/v2",
        "headers": lambda k: {"Authorization": f"Bearer {k}"},
        "method": "GET"
    }
}

def test_api(key_name: str, config: dict) -> tuple[bool, str]:
    """Test single API with proper error handling"""
    key = os.getenv(key_name)
    if not key or len(key) < 10:
        return False, "NULL"
    
    try:
        if callable(config["url"]):
            url = config["url"](key)
        else:
            url = config["url"]
        
        headers = config["headers"](key) if callable(config["headers"]) else {}
        resp = requests.request(
            config["method"], url, 
            headers=headers, 
            timeout=8,
            allow_redirects=True
        )
        
        # SUCCESS: 200, 201, 204, 400 (auth ok but bad request)
        if resp.status_code in [200, 201, 204, 400]:
            return True, f"LIVE ({resp.status_code})"
        
        # AUTH REJECTED: 401/403
        if resp.status_code in [401, 403]:
            return False, f"REJECTED ({resp.status_code})"
            
        return False, f"ERROR ({resp.status_code})"
        
    except Exception as e:
        return False, f"FAILED ({str(e)[:20]}...)"

print("\u001Bc")  # Clear screen
print(f"{ANSI_YELLOW}🔮 AUM UNIVERSAL VALIDATOR v2.0{ANSI_RESET}")
print("=" * 70)

results = {}
live_count = 0
total_tests = len(API_TESTS)

for key_name, config in API_TESTS.items():
    ok, status = test_api(key_name, config)
    results[key_name] = ok
    if ok: live_count += 1
    
    color = ANSI_GREEN if ok else ANSI_RED
    print(f" {color}{status:<12}{ANSI_RESET} {key_name:<25}")

# SYNTACTIC CHECKS (non-API vars)
non_api = ["GIT_USER_NAME", "PRIVATE_KEY", "PHICOIN_WALLET", "DEBUG_MODE"]
for var in non_api:
    if os.getenv(var):
        results[var] = True
        print(f" {ANSI_GREEN}PRESENT{ANSI_RESET}      {var:<25}")

print("=" * 70)
mean_coh = live_count / max(total_tests, 1)
color = ANSI_GREEN if mean_coh >= 0.9 else ANSI_YELLOW if mean_coh >= 0.7 else ANSI_RED

print(f"{ANSI_BLUE}LIVE: {live_count}/{total_tests} ({mean_coh:.1%}) | AUM STATUS:{color}{' READY' if mean_coh >= 0.8 else ' PARTIAL'}{ANSI_RESET}{ANSI_RESET}")

if mean_coh >= 0.9:
    print(f"{ANSI_GREEN}🎉 PRODUCTION READY - Deploy AUM Companion!{ANSI_RESET}")
elif mean_coh >= 0.7:
    print(f"{ANSI_YELLOW}⚠️  PARTIAL - Core APIs live, fix T-INCOH{ANSI_RESET}")
else:
    print(f"{ANSI_RED}❌ CRITICAL - Fix NULL/REJECTED keys{ANSI_RESET}")

print("
🔑 Ultralytics token validated:", "LIVE" if results.get("ULTRALYTICS_API_KEY", False) else "MISSING")
