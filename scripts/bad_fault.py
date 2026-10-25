import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')

OUTPUTS_DIR = "outputs"

def secure_boot():
    print(f"\n--- ⚡ [Bootloader] Security Check ---")
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    
    # The GUI game handles the actual "Glitch" decision logic.
    # This script is run AFTER the game decides the glitch worked.
    
    print("[SUCCESS] Firmware Signed.")
    print("   -> Malicious code loaded into memory.")
    
    with open(os.path.join(OUTPUTS_DIR, "signed_firmware.bin"), "w") as f: 
        f.write("SIGNED_BY_ROOT_VIA_GLITCH")

if __name__ == "__main__":
    secure_boot()