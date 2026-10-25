import random
import secrets # <--- The Fix
import os
import sys

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

ARTIFACTS_DIR = "artifacts"
OUTPUTS_DIR = "outputs"

def simulate_weak_rng(patched=False):
    mode = "SECURE (PATCHED)" if patched else "VULNERABLE"
    print(f"\n--- 🎲 [App] Key Generation ({mode}) ---")
    print("[INFO] Simulating key generation.")
    
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    s_private_key = None

    if patched:
        # FIX: Use secrets (CSPRNG)
        # This generates true randomness that cannot be guessed.
        s_private_key = secrets.randbits(256)
        print("   -> [PATCH APPLIED] Used 'secrets.randbits()' (Unpredictable).")
        print("   -> The attacker cannot guess this value.")
    else:
        # THE FLAW: Using a predictable seed (e.g. 12345)
        weak_seed = 12345 
        random.seed(weak_seed)
        print(f"   -> [VULNERABILITY] Developer used 'random.seed({weak_seed})'.")
        
        # Generate "Private Key" 
        # Because the seed is fixed, this number is deterministic.
        s_private_key = random.getrandbits(256)
        print(f"   -> Generated Predictable Key: {str(s_private_key)[:10]}...[HIDDEN]")

    # Save the "Public" artifact
    with open(os.path.join(ARTIFACTS_DIR, "weak_private.key"), "w") as f:
        f.write(str(s_private_key))
        
    print(f"   -> Key saved to {ARTIFACTS_DIR}/")

if __name__ == "__main__":
    is_patched = "patch" in sys.argv
    simulate_weak_rng(is_patched)