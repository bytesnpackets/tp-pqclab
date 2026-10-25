# PQCLab: Post-Quantum Cryptography Implementation Lab

School project: Security Technology and Innovation (STI), Diploma in Cybersecurity & Digital Forensics, Temasek Polytechnic (Oct to Dec 2025). Group project; this repo is the Linux source of the demonstrator.

Post-quantum algorithms are only as safe as their implementation. PQCLab is a Tkinter GUI that runs a correct post-quantum signature flow next to deliberately flawed ones, then shows how each flaw is attacked.

| Flaw demonstrated | Weak script | Attack script |
|---|---|---|
| Predictable randomness | `scripts/bad_rng.py` | `scripts/attack_rng.py` |
| Timing side channel | `scripts/bad_timing.py` | `scripts/attack_timing.py` |
| Algorithm downgrade | `scripts/bad_downgrade.py` | `scripts/attack.py` |
| Fault injection | `scripts/bad_fault.py` | |
| Secure baseline | `scripts/good_sign.py` | |

## Run (Ubuntu/Linux)
```bash
chmod +x setup.sh run.sh
./setup.sh   # installs build tools, liboqs and a Python venv (needs sudo)
./run.sh
```

Educational demo only. Do not use the weak implementations in real systems.
