import time
import sys
import os

# Force UTF-8 for Windows
sys.stdout.reconfigure(encoding='utf-8')

SECRET_PIN = "9481"  # A 4-digit PIN the attacker wants to guess

def secure_compare(user_input):
    # THE FLAW: "Early Exit" string comparison
    # It returns FALSE immediately when a character is wrong.
    # It takes LONGER if the character is right.
    for i in range(len(SECRET_PIN)):
        if i >= len(user_input): return False
        
        # Simulate processing time for a match
        if user_input[i] == SECRET_PIN[i]:
            time.sleep(0.2) # SLEEP 0.2s for every correct digit
        else:
            return False # Wrong digit? Return immediately.
            
    return True

def simulate_timing_leak():
    print("\n--- ⏱️  [Flawed App] Timing Side-Channel Simulation ---")
    print("[INFO] Simulating a PIN check that is vulnerable to Timing Analysis.")
    print(f"[SECRET] The real PIN is hidden in memory (Length: {len(SECRET_PIN)} digits).")
    
    # We create a dummy "interface" file for the attacker to write guesses to
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/timing_interface.txt", "w") as f:
        f.write("READY")

    print("[STATUS] Waiting for input from Attacker...")

if __name__ == "__main__":
    simulate_timing_leak()