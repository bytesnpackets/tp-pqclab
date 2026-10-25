import os
import sys

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

ARTIFACTS_DIR = "artifacts"
OUTPUTS_DIR = "outputs"

def run_attack():
    print("\n--- 🔥 [Attacker Tool] Attack Started ---")
    print("[INFO] Exploiting 'Nonce Reuse' to recover Private Key.\n")
    
    # 1. Load Data
    try:
        print("[STEP 1] Intercepting Public Data...")
        with open(os.path.join(OUTPUTS_DIR, "z1.sig"), "r") as f: z1 = int(f.read())
        with open(os.path.join(OUTPUTS_DIR, "z2.sig"), "r") as f: z2 = int(f.read())
        with open(os.path.join(OUTPUTS_DIR, "c1.hash"), "r") as f: c1 = int(f.read())
        with open(os.path.join(OUTPUTS_DIR, "c2.hash"), "r") as f: c2 = int(f.read())
        print("   -> Intercepted Signature 1 (z1) and Challenge 1 (c1)")
        print("   -> Intercepted Signature 2 (z2) and Challenge 2 (c2)")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return

    # 2. The Math Explanation
    print("\n[STEP 2] Analyzing the Math...")
    print("   -> We know: z = y + (c * s)")
    print("   -> If 'y' was REUSED, we can subtract: (z1 - z2) = (c1 - c2) * s")
    print("   -> Solving for 's' (Private Key)...")

    # 3. The Calculation
    print("\n[STEP 3] Performing Key Recovery...")
    
    numerator = z1 - z2
    denominator = c1 - c2
    
    if denominator == 0:
        print("❌ Attack failed: Challenges were identical.")
        return
        
    # Integer division
    s_recovered = numerator // denominator
    print(f"   -> Division result: s = (z1-z2) / (c1-c2)")
    
    # Save candidate temporarily
    recovered_key_path = os.path.join(OUTPUTS_DIR, "recovered_private.key")
    with open(recovered_key_path, "w") as f: f.write(str(s_recovered))

    # 4. Verification
    print("\n[STEP 4] Verifying the Stolen Key...")
    try:
        with open(os.path.join(ARTIFACTS_DIR, "bad_private.key"), "r") as f:
            s_real = int(f.read())
        
        if s_recovered == s_real:
            print("\n" + "="*40)
            print("  🔥🔥🔥 ATTACK SUCCESSFUL! 🔥🔥🔥")
            print("  The math holds true. The private key is yours.")
            print("="*40 + "\n")
        else:
            # If keys don't match, it means the Nonce was NOT reused (Patch worked)
            print("\n" + "x"*50)
            print("  ❌ ATTACK FAILED: Calculated key is invalid.")
            print("  The system used unique nonces, breaking the linear algebra.")
            print("x"*50 + "\n")
            # Clean up the invalid file so GUI knows it failed
            if os.path.exists(recovered_key_path):
                os.remove(recovered_key_path)
                
    except:
        print("❌ Verification failed (Real key not found).")

if __name__ == "__main__":
    run_attack()