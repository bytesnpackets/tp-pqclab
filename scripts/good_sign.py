import sys
import os

# Force UTF-8 for Windows consoles (Emojis support)
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
SIG_ALGORITHM = "Dilithium2"
ARTIFACTS_DIR = "artifacts"
MESSAGE = b"This is a secure message for the 'good' demo."

def run_good_demo():
    print(f"\n--- 🛡️  Running GOOD Implementation Demo ({SIG_ALGORITHM}) ---")
    print("[INFO] Purpose: Demonstrate a standard, secure PQC signature process.\n")

    # Safe Import for Windows Users without C++ Tools
    try:
        import oqs
    except ImportError:
        print("❌ FATAL ERROR: The 'oqs' library is not installed.")
        print("   This happens on Windows if 'Visual C++ Build Tools' are missing.")
        print("   You can still run Experiment B (Bad Demo) as it uses Python simulation!")
        return

    # 1. Check Algorithm
    try:
        enabled_sigs = oqs.get_enabled_sig_mechanisms()
        if SIG_ALGORITHM not in enabled_sigs:
            print(f"❌ ERROR: '{SIG_ALGORITHM}' not enabled.")
            return
    except Exception as e:
        print(f"❌ ERROR: OQS Library issue: {e}")
        return
    
    print(f"[STEP 1] Algorithm '{SIG_ALGORITHM}' selected.")
    print("   -> This algorithm is NIST-standardized for quantum safety.")

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    
    try:
        signer = oqs.Signature(SIG_ALGORITHM)
    except Exception as e:
        print(f"Error initializing: {e}")
        return

    # 2. Key Generation
    print("\n[STEP 2] Generating Keypair...")
    public_key = signer.generate_keypair()
    private_key = signer.export_secret_key()
    print(f"   -> Public Key Size: {len(public_key)} bytes")
    print(f"   -> Private Key Size: {len(private_key)} bytes")
    print("   -> [NOTE] The library automatically handles random seed generation here.")

    # Use os.path.join for Windows paths
    priv_key_path = os.path.join(ARTIFACTS_DIR, "good_private.key")
    pub_key_path = os.path.join(ARTIFACTS_DIR, "good_public.key")
    
    with open(pub_key_path, "wb") as f:
        f.write(public_key)
    with open(priv_key_path, "wb") as f:
        f.write(private_key)
    print(f"   -> Keys saved to {ARTIFACTS_DIR}/")

    # 3. Signing
    print(f"\n[STEP 3] Signing Message: '{MESSAGE.decode()}'")
    signature = signer.sign(MESSAGE)
    print(f"   -> Signature created ({len(signature)} bytes).")
    print("   -> [CRITICAL] A unique, random 'nonce' was used internally.")
    print("   -> Because the nonce is unique, the Private Key remains safe.")

    # 4. Verifying
    print("\n[STEP 4] Verifying Signature...")
    print("   -> The verifier takes: Message + Signature + Public Key")
    verifier = oqs.Signature(SIG_ALGORITHM)
    is_valid = verifier.verify(MESSAGE, signature, public_key)
    
    if is_valid:
        print("\n✅ SUCCESS: Signature is VALID.")
        print("   -> Mathematical Proof: The signature corresponds to the public key.")
        print("   -> Integrity Proof: The message has not been altered.")
    else:
        print("\n❌ FAILURE: Signature is INVALID.")

if __name__ == "__main__":
    run_good_demo()