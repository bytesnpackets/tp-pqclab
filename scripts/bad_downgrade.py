import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

def simulate_downgrade():
    print("\n--- 📉 [Network] Connection Simulation Started ---")
    print("[INFO] Simulating a handshake between Client and Server.")
    
    # 1. CLIENT HELLO
    print("\n[STEP 1] Client sends 'ClientHello'")
    print("   -> Supported Ciphers: [Dilithium2 (PQC), RSA-2048 (Legacy)]")
    print("   -> Preference: Dilithium2")
    
    time.sleep(0.5)
    
    # 2. ATTACKER INTERCEPTION
    print("\n[STEP 2] 🔥 ATTACKER INTERCEPTS TRAFFIC 🔥")
    print("   -> Action: Modifying 'ClientHello' packet.")
    print("   -> Removing 'Dilithium2' from supported list.")
    print("   -> Forwarding modified packet to Server.")
    
    time.sleep(0.5)
    
    # 3. SERVER RESPONSE
    print("\n[STEP 3] Server receives modified 'ClientHello'")
    print("   -> Server sees: [RSA-2048]")
    print("   -> Server Action: Must select RSA-2048.")
    print("   -> Server sends 'ServerHello' (Selected: RSA-2048)")
    
    time.sleep(0.5)
    
    # 4. RESULT
    print("\n" + "="*40)
    print("  ⚠️  DOWNGRADE SUCCESSFUL  ⚠️")
    print("  The connection is now encrypted with RSA.")
    print("  This traffic can be decrypted by a Quantum Computer.")
    print("="*40 + "\n")

if __name__ == "__main__":
    simulate_downgrade()