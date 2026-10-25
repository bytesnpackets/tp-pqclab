import random
import os
import sys

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

ARTIFACTS_DIR = "artifacts"
OUTPUTS_DIR = "outputs"

def run_rng_attack():
    print("\n--- 🔥 [Attacker Tool] RNG Brute-Force Started ---")
    print("[INFO] Attempting to guess the seed used to generate the key.\n")
    
    # 1. Load the Target Key (The one we want to steal)
    target_key = None
    try:
        with open(os.path.join(ARTIFACTS_DIR, "weak_private.key"), "r") as f:
            target_key_str = f.read().strip()
            if not target_key_str:
                print("❌ Error: Target key file is empty.")
                return
            target_key = int(target_key_str)
    except FileNotFoundError:
        print("❌ Error: Target key not found. Run the App first.")
        return

    print(f"[STEP 1] Target Key identified: {str(target_key)[:15]}...")
    print("[STEP 2] Scanning seeds (10000 - 15000) to find a match...")
    
    found_key = None
    
    # REAL ATTACK LOGIC:
    # We try every seed. If the key generated matches the target, we win.
    # If the target was generated securely (patched with 'secrets'), NO seed will match.
    for seed_guess in range(10000, 15000):
        random.seed(seed_guess)
        candidate_key = random.getrandbits(256)
        
        if candidate_key == target_key:
            print(f"   -> [MATCH FOUND!] Seed {seed_guess} generates the target key.")
            found_key = candidate_key
            break
            
    # REPORT RESULTS
    if found_key:
        print("\n[STEP 3] Regenerating Private Key...")
        
        with open(os.path.join(OUTPUTS_DIR, "recovered_rng_key.key"), "w") as f:
            f.write(str(found_key))
            
        print("\n" + "="*40)
        print("  🔥🔥🔥 ATTACK SUCCESSFUL! 🔥🔥🔥")
        print("  The key was regenerated using the weak seed.")
        print("="*40 + "\n")
    else:
        # This happens when the system is PATCHED
        print("\n" + "x"*50)
        print("  ❌ ATTACK FAILED: No matching seed found.")
        print("  The target key appears to be truly random (Secure).")
        print("  The brute-force attempt was unsuccessful.")
        print("x"*50 + "\n")
        
        # Cleanup evidence
        if os.path.exists(os.path.join(OUTPUTS_DIR, "recovered_rng_key.key")):
            os.remove(os.path.join(OUTPUTS_DIR, "recovered_rng_key.key"))

if __name__ == "__main__":
    run_rng_attack()