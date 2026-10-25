import os
import secrets
import sys

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

ARTIFACTS_DIR = "artifacts"
OUTPUTS_DIR = "outputs"

def simulate_flawed_signing(patched=False):
    mode = "SECURE (PATCHED)" if patched else "VULNERABLE"
    print(f"\n--- ☠️  [App] Signing Simulation ({mode}) ---")
    
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    # 1. SIMULATE KEY & NONCE GENERATION
    # In real Dilithium, these are complex polynomials.
    # For education, we use large integers to demonstrate the logic.
    s_private_key = secrets.randbits(256)
    
    # Initial Nonce
    y_nonce = secrets.randbits(256)
    
    if not patched:
        print(f"   -> Generated Random Nonce 'y': {y_nonce}...")
        print("   -> [WARNING] This 'y' should be regenerated for every signature!")

    # 2. SIMULATE SIGNING TWO MESSAGES
    
    # Message 1
    c1_challenge = secrets.randbits(128)
    z1_signature = y_nonce + (c1_challenge * s_private_key)
    
    # Message 2
    c2_challenge = secrets.randbits(128)
    
    if patched:
        # FIX: Generate a NEW nonce for the second message
        y_nonce_2 = secrets.randbits(256) 
        z2_signature = y_nonce_2 + (c2_challenge * s_private_key)
        print("   -> [PATCH APPLIED] Regenerated Nonce for 2nd signature.")
        print("   -> The attacker's math (z1-z2) will now fail.")
    else:
        # FLAW: Reuse the old nonce
        z2_signature = y_nonce + (c2_challenge * s_private_key)
        print("   -> [VULNERABILITY] Reused Nonce 'y' for 2nd signature.")
        print("   -> [CRITICAL ERROR] The math is now broken.")

    # 3. SAVE DATA
    with open(os.path.join(OUTPUTS_DIR, "z1.sig"), "w") as f: f.write(str(z1_signature))
    with open(os.path.join(OUTPUTS_DIR, "z2.sig"), "w") as f: f.write(str(z2_signature))
    with open(os.path.join(OUTPUTS_DIR, "c1.hash"), "w") as f: f.write(str(c1_challenge))
    with open(os.path.join(OUTPUTS_DIR, "c2.hash"), "w") as f: f.write(str(c2_challenge))
    
    # Save Real Key for verification later
    with open(os.path.join(ARTIFACTS_DIR, "bad_private.key"), "w") as f: f.write(str(s_private_key))
        
    print(f"   -> Public artifacts saved to {OUTPUTS_DIR}/")

if __name__ == "__main__":
    # Check for command line argument "patch"
    is_patched = "patch" in sys.argv
    simulate_flawed_signing(is_patched)