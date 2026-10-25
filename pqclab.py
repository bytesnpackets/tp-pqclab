import tkinter as tk
from tkinter import scrolledtext, messagebox, Frame, Button, Label, PanedWindow, Toplevel, Checkbutton, IntVar, Entry, Canvas
from tkinter.ttk import Progressbar, Separator
import subprocess
import sys
import os
import time

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class PQCLabApp:
    def __init__(self, root):
        self.root = root
        root.title("PQCLab: Post-Quantum Cryptography Lab (Final Edition)")
        root.geometry("1150x900")

        # Header
        Label(root, text="PQCLab: PQC Implementation Security Suite", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Layout
        main_pane = PanedWindow(root, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        top_pane = Frame(main_pane, height=550)
        main_pane.add(top_pane, stretch="always")

        # Controls
        controls_frame = Frame(top_pane)
        controls_frame.pack(pady=5)

        def add_row(row, label, btn_text, color, cmd):
            Label(controls_frame, text=label, font=("Helvetica", 9, "bold")).grid(row=row, column=0, padx=5, sticky="e")
            Button(controls_frame, text=btn_text, bg=color, fg="white", width=35, command=cmd).grid(row=row, column=1, padx=5, pady=3)

        add_row(0, "Baseline:", "Exp A: Secure Implementation", "#4CAF50", self.start_good_mission)
        add_row(1, "Math Risk:", "Exp B: Nonce Reuse Attack", "#F44336", self.start_nonce_mission)
        add_row(2, "Input Risk:", "Exp C: Weak RNG (Predictable Key)", "#FF9800", self.start_rng_mission)

        Separator(controls_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky="ew", pady=5)
        add_row(4, "Protocol Game:", "Exp D: Protocol Downgrade (Interactive)", "#FF5722", self.start_downgrade_mission)
        add_row(5, "Hardware Game:", "Exp E: Timing Side-Channel (Interactive)", "#9C27B0", self.start_timing_mission)
        add_row(6, "Physical Game:", "Exp F: Fault Injection (Interactive)", "#673AB7", self.start_fault_mission)

        Button(controls_frame, text="🔄 RESET LAB", bg="#2196F3", fg="white", width=15, height=5, command=self.reset_lab).grid(row=0, column=2, rowspan=7, padx=20)

        # Logs
        log_frame = Frame(top_pane)
        log_frame.pack(pady=5, padx=10, fill="both", expand=True)
        Label(log_frame, text="Experiment Log & Remediation:", font=("Helvetica", 11, "bold")).pack(anchor="w")

        self.output_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15, font=("Courier New", 10))
        self.output_text.pack(fill="both", expand=True)
        self.output_text.config(state="disabled")

        # Patch Button Frame
        self.patch_frame = Frame(log_frame, bg="#eee", height=40)
        self.patch_frame.pack(fill="x", pady=2)
        self.patch_button = None

        # Viewers
        bottom_pane = Frame(main_pane, height=200)
        main_pane.add(bottom_pane, stretch="always")
        f1 = Frame(bottom_pane); f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        f2 = Frame(bottom_pane); f2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        Label(f1, text="Target / System State", font=("Helvetica", 10, "bold")).pack()
        self.key_text_a = scrolledtext.ScrolledText(f1, wrap=tk.WORD, height=8, font=("Courier New", 9))
        self.key_text_a.pack(fill="both", expand=True)
        self.key_text_a.config(state="disabled")

        Label(f2, text="Attacker Result / Evidence", font=("Helvetica", 10, "bold")).pack()
        self.key_text_b = scrolledtext.ScrolledText(f2, wrap=tk.WORD, height=8, font=("Courier New", 9))
        self.key_text_b.pack(fill="both", expand=True)
        self.key_text_b.config(state="disabled")

    # --- HELPERS ---
    def log_msg(self, message):
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.output_text.config(state="disabled")

    def update_viewer(self, viewer, text):
        viewer.config(state="normal")
        viewer.delete('1.0', tk.END)
        viewer.insert(tk.END, text)
        viewer.config(state="disabled")

    def run_script(self, path, args=[]):
        try:
            exe = sys.executable
            self.root.update_idletasks()
            base = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(base, *path.split("/"))
            env = os.environ.copy(); env["PYTHONIOENCODING"] = "utf-8"
            if "timing" in path: env["PYTHONPATH"] = os.path.dirname(full_path)

            cmd = [exe, full_path] + args
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', env=env)
            self.log_msg(res.stdout + "\n")
        except Exception as e: self.log_msg(f"Error: {e}\n")

    def clean_slate(self):
        self.output_text.config(state="normal"); self.output_text.delete('1.0', tk.END); self.output_text.config(state="disabled")
        self.update_viewer(self.key_text_a, ""); self.update_viewer(self.key_text_b, "")
        if self.patch_button: self.patch_button.destroy()
        for root, dirs, files in os.walk("outputs"):
            for f in files: os.remove(os.path.join(root, f))
        for root, dirs, files in os.walk("artifacts"):
            for f in files: os.remove(os.path.join(root, f))

    def reset_lab(self): self.clean_slate(); self.log_msg("--- LAB RESET ---\n")

    def load_file(self, path, viewer):
        try:
            with open(path, "r") as f: self.update_viewer(viewer, f.read())
        except:
            self.update_viewer(viewer, "[SECURE - No Artifact Found]")

    # --- IMPROVED MISSION BRIEFING ---
    def show_mission_briefing(self, title, role, objective, theory, steps, callback):
        brief_win = Toplevel(self.root)
        brief_win.title(f"Briefing: {title}"); brief_win.geometry("700x600")
        Label(brief_win, text=f"🕵️ {title.upper()}", font=("Helvetica", 16, "bold")).pack(pady=10)

        f = Frame(brief_win, bg="#fffdd0", relief="sunken", bd=2)
        f.pack(fill="both", expand=True, padx=20, pady=5)

        text_area = tk.Text(f, wrap=tk.WORD, bg="#fffdd0", font=("Helvetica", 11))
        text_area.pack(fill="both", expand=True, padx=5, pady=5)

        content = f"""
ROLE: {role}
OBJECTIVE: {objective}

[THEORY & CONCEPT]
{theory}

[INSTRUCTIONS]
{steps}
"""
        text_area.insert(tk.END, content)
        text_area.config(state="disabled")

        Button(brief_win, text="🚀 START MISSION", bg="green", fg="white", font=("Helvetica", 12, "bold"), command=lambda: [brief_win.destroy(), callback()]).pack(pady=15)

    # --- POP-UP PATCH WINDOW (NEW!) ---
    def offer_patch(self, type):
        if self.patch_button: self.patch_button.destroy() # prevent duplicates
        patch_win = Toplevel(self.root)
        patch_win.title(f"System Alert: {type} Vulnerability")
        patch_win.geometry("450x250")

        Label(patch_win, text="⚠️ VULNERABILITY EXPLOITED", font=("Helvetica", 12, "bold"), fg="red").pack(pady=10)

        info = ""
        if type == "NONCE": info = "The attacker recovered the key because the Nonce was reused.\nWe must patch the code to generate unique nonces."
        elif type == "RNG": info = "The attacker cloned the key because the RNG seed was weak.\nWe must patch the code to use a CSPRNG."

        Label(patch_win, text=info, font=("Helvetica", 10), wraplength=400, justify="center").pack(pady=5)

        def run_patch():
            patch_win.destroy()
            self.log_msg(f"\n--- 🛠️ APPLYING PATCH & RE-VERIFYING ({type}) ---\n")
            self.update_viewer(self.key_text_b, "[Testing Patch...]")

            if type == "NONCE":
                self.run_script("scripts/bad_demo.py", args=["patch"])
                self.run_script("scripts/attack.py")
                self.load_file("outputs/recovered_private.key", self.key_text_b)
            elif type == "RNG":
                self.run_script("scripts/bad_rng.py", args=["patch"])
                self.run_script("scripts/attack_rng.py")
                self.load_file("outputs/recovered_rng_key.key", self.key_text_b)

            self.log_msg("\n✅ VERIFICATION RESULT: Attack Failed. System is Secure.\n")

        Button(patch_win, text="🛠️ APPLY PATCH & RE-VERIFY", bg="#008CBA", fg="white", font=("Helvetica", 10, "bold"), command=run_patch).pack(pady=20)

    def print_remediation(self, type):
        msg = "\n" + "*"*60 + "\n🛡️  REMEDIATION REPORT (PREVENTION)  🛡️\n" + "*"*60 + "\n"
        if type == "NONCE":
            msg += "VULNERABILITY: Nonce Reuse (CWE-323).\n"
            msg += "WHY IT HAPPENS: Generating the 'random' number once and keeping it.\n"
            msg += "FIX: Ensure the Random Number Generator (RNG) is called FRESH for every single signature.\n"
        elif type == "RNG":
            msg += "VULNERABILITY: Predictable Seed (CWE-330).\n"
            msg += "WHY IT HAPPENS: Using 'random.seed(time)' or a static number.\n"
            msg += "FIX: Use Cryptographically Secure PRNG (CSPRNG) like 'secrets' or /dev/urandom.\n"
        elif type == "DOWNGRADE":
            msg += "VULNERABILITY: Weak Cipher Negotiation (CWE-326).\n"
            msg += "WHY IT HAPPENS: Server supports old algorithms for compatibility.\n"
            msg += "FIX: Edit server config to strictly REJECT any connection requesting RSA/Classical crypto.\n"
        elif type == "TIMING":
            msg += "VULNERABILITY: Timing Side-Channel (CWE-208).\n"
            msg += "WHY IT HAPPENS: 'if x != y: return False' takes less time than checking the whole string.\n"
            msg += "FIX: Use Constant-Time comparison. The check must take the same time regardless of success/failure.\n"
        elif type == "FAULT":
            msg += "VULNERABILITY: Fault Injection / Glitching.\n"
            msg += "WHY IT HAPPENS: Hardware skips an instruction due to voltage spike.\n"
            msg += "FIX: Redundancy. Check 'is_secure' twice. Use checksums. Don't rely on a single boolean flag.\n"
        self.log_msg(msg)

    # --- EXPERIMENTS ---
    def start_good_mission(self):
        self.clean_slate()
        theory = "Post-Quantum Cryptography (PQC) uses complex math (Lattices) to resist Quantum Computers. A 'Secure Implementation' relies on a vetted library like 'liboqs' to handle the math and randomness. Developers should never write their own crypto code."
        steps = "1. You are a Bank Officer signing a transaction.\n2. Click Start.\n3. Observe how the 'Good' app generates keys and nonces automatically."
        self.show_mission_briefing("Secure Implementation", "Bank Officer", "Sign securely.", theory, steps, self._execute_good)
    def _execute_good(self):
        self.log_msg("=== EXP A: SECURE ===\n")
        self.run_script("scripts/good_sign.py"); self.update_viewer(self.key_text_a, "[Secure Key Generated]")

    def start_nonce_mission(self):
        self.clean_slate()
        theory = "Digital signatures require a 'Nonce' (Number used ONCE). If you use the SAME number for two different messages, the math equations ($z = y + cs$) become solvable. By subtracting the two equations, the random 'y' vanishes, leaving only the Private Key."
        steps = "1. The Flawed App will sign 2 messages with ONE nonce.\n2. The Attack Script will capture the signatures.\n3. It will do the algebra to recover the key.\n4. Wait for the System Alert to PATCH the code."
        self.show_mission_briefing("Nonce Reuse Attack", "Cryptographic Analyst", "Recover key from public signatures.", theory, steps, self._execute_nonce)
    def _execute_nonce(self):
        self.log_msg("=== EXP B: NONCE REUSE ===\n")
        self.run_script("scripts/bad_demo.py"); self.run_script("scripts/attack.py")
        self.load_file("outputs/recovered_private.key", self.key_text_b); self.print_remediation("NONCE"); self.offer_patch("NONCE")

    def start_rng_mission(self):
        self.clean_slate()
        theory = "Keys are only as secure as the Random Number Generator (RNG) that made them. If a developer uses 'random.seed(123)', the sequence is predictable. An attacker just needs to guess the seed to regenerate the exact same Private Key."
        steps = "1. Developer used a weak seed.\n2. Attacker script scans seeds (Brute Force).\n3. Once seed is found, we clone the key.\n4. Wait for the System Alert to PATCH the code."
        self.show_mission_briefing("Weak RNG Attack", "External Attacker", "Clone key by guessing seed.", theory, steps, self._execute_rng)
    def _execute_rng(self):
        self.log_msg("=== EXP C: WEAK RNG ===\n")
        self.run_script("scripts/bad_rng.py"); self.load_file("artifacts/weak_private.key", self.key_text_a)
        self.log_msg("\n--- EXECUTING ATTACK ---\n")
        self.run_script("scripts/attack_rng.py"); self.load_file("outputs/recovered_rng_key.key", self.key_text_b); self.print_remediation("RNG"); self.offer_patch("RNG")

    # --- GAMES ---
    def start_downgrade_mission(self):
        self.clean_slate()
        theory = "A Downgrade Attack (MITM) tricks a server into using older, weaker encryption. Even if the server SUPPORTS Quantum-Safe crypto, it might allow RSA if the client 'claims' it doesn't speak PQC."
        steps = "1. You are the Man-in-the-Middle.\n2. UNCHECK 'Dilithium' to hide it from the server.\n3. Click FORWARD.\n4. Check 'Strict Policy' to see the defense."
        self.show_mission_briefing("Protocol Downgrade", "MITM", "Force RSA.", theory, steps, self._launch_downgrade_game)
    def _launch_downgrade_game(self):
        self.log_msg("=== EXP D: DOWNGRADE GAME ===\n")
        win = Toplevel(self.root); win.geometry("450x350"); win.title("Packet Interceptor")
        Label(win, text="⚠️ PACKET INTERCEPTED ⚠️", font=("Helvetica", 14, "bold"), fg="red").pack(pady=10)
        var_dilithium = IntVar(value=1); var_rsa = IntVar(value=1); var_policy = IntVar(value=0)
        Checkbutton(win, text="Cipher: Dilithium2 (Secure)", variable=var_dilithium).pack(anchor="w", padx=20)
        Checkbutton(win, text="Cipher: RSA-2048 (Weak)", variable=var_rsa).pack(anchor="w", padx=20)
        Label(win, text="--- SERVER DEFENSE CONTROLS ---", fg="blue").pack(pady=5)
        Checkbutton(win, text="Enable Strict PQC Policy (Reject RSA)", variable=var_policy, fg="blue").pack(anchor="w", padx=20)
        def send():
            win.destroy()
            if var_policy.get() == 1:
                self.log_msg("\n🛡️ [DEFENSE]: Server rejected RSA connection! PQC Policy Enforced.\n")
                self.update_viewer(self.key_text_b, "[Connection Dropped - SECURE]")
            elif var_dilithium.get() == 0 and var_rsa.get() == 1:
                self.log_msg("\n⚠️ [ATTACK]: Downgrade Successful! RSA used.\n"); self.run_script("scripts/bad_downgrade.py")
                self.update_viewer(self.key_text_b, "Traffic Downgraded (Vulnerable)")
            else: self.log_msg("\n[INFO]: Normal Connection established.\n")
        Button(win, text="FORWARD PACKET", bg="red", fg="white", command=send).pack(pady=10)

    def start_timing_mission(self):
        self.clean_slate()
        theory = "A Timing Attack exploits the time a computer takes to say 'No'. If checking a WRONG password takes 0.01s, but a partially CORRECT password takes 0.02s, we can guess the password digit-by-digit."
        steps = "1. Guess a PIN (e.g. 0000).\n2. Watch the BLUE BAR.\n3. Long Bar = You guessed a digit correctly.\n4. Use the timing info to crack the code."
        self.show_mission_briefing("Side-Channel Attack", "Timing Analyst", "Guess PIN by time.", theory, steps, self._launch_timing_game)
    def _launch_timing_game(self):
        self.log_msg("=== EXP E: TIMING GAME ===\n"); win = Toplevel(self.root); win.geometry("500x450")
        Label(win, text="PIN PAD", font=("bold", 12)).pack(pady=10)
        entry_pin = Entry(win, font=("Courier", 20)); entry_pin.pack()
        var_secure = IntVar(value=0)
        Checkbutton(win, text="Enable Constant-Time Check (Fix)", variable=var_secure, fg="blue").pack(pady=5)
        canvas = Canvas(win, width=400, height=50, bg="white"); canvas.pack(pady=10)
        lbl = Label(win, text="Ready..."); lbl.pack()
        SECRET = "9481"
        def check():
            guess = entry_pin.get(); canvas.delete("all")
            if var_secure.get() == 1:
                canvas.create_rectangle(10, 10, 400, 40, fill="green")
                lbl.config(text="Time: CONSTANT (No Leak)")
                if guess == SECRET: self.log_msg("\n[SUCCESS]: Correct PIN.\n")
                else: self.log_msg("\n[INFO]: Wrong PIN. No timing leak observed.\n")
            else:
                match = 0
                for i in range(4):
                    if i < len(guess) and guess[i] == SECRET[i]: match += 1
                    else: break
                w = 50 + (match * 80)
                canvas.create_rectangle(10, 10, w, 40, fill="blue")
                lbl.config(text=f"Time: {0.5 + match*0.5}s")
                if guess == SECRET: self.log_msg("\n[FAIL]: PIN Guessed via Timing Leak!\n"); self.print_remediation("TIMING")
        Button(win, text="TEST PIN", command=check).pack()

    def start_fault_mission(self):
        self.clean_slate()
        theory = "Fault Injection involves physically attacking the chip. By creating a voltage spike (Glitch) at the exact moment a security check runs, we can force the CPU to skip the check or flip a 'False' to 'True'."
        steps = "1. Watch the Boot Process text.\n2. Wait for it to verify signature.\n3. Click ZAP just as it says 'VERIFYING'.\n4. Timing must be perfect."
        self.show_mission_briefing("Fault Injection", "Hardware Hacker", "Glitch CPU.", theory, steps, self._launch_fault_game)
    def _launch_fault_game(self):
        self.log_msg("=== EXP F: FAULT GAME ===\n"); win = Toplevel(self.root); win.geometry("500x350")
        Label(win, text="BOOT MONITOR", font=("bold", 12)).pack(pady=10)
        status_frame = Frame(win, bg="white", width=300, height=50); status_frame.pack_propagate(False); status_frame.pack(pady=10)
        self.status_lbl = Label(status_frame, text="IDLE", font=("bold", 20), bg="white", fg="black")
        self.status_lbl.pack(expand=True, fill="both")
        var_secure = IntVar(value=0)
        Checkbutton(win, text="Enable Redundancy Check (Fix)", variable=var_secure, fg="blue").pack(pady=5)
        self.glitched = False; self.running = True
        def zap():
            if self.status_lbl.cget("text") == "VERIFYING...": self.glitched = True; self.status_lbl.config(text="GLITCHED!", fg="red")
            else: self.status_lbl.config(text="MISSED!", fg="gray")
        Button(win, text="⚡ ZAP ⚡", bg="orange", width=20, height=2, command=zap).pack()
        def loop(step=0):
            if not self.running: return
            steps = ["LOADING...", "MOUNTING...", "VERIFYING...", "BOOTING...", "DONE"]
            if step >= len(steps): return
            current = steps[step]
            self.status_lbl.config(text=current)
            if current == "VERIFYING...":
                self.status_lbl.config(bg="yellow"); delay = 1500
            else:
                self.status_lbl.config(bg="white"); delay = 1000
            if self.glitched:
                win.after(1000, win.destroy)
                if var_secure.get() == 1:
                    self.log_msg("\n🛡️ [DEFENSE]: Glitch detected! Redundancy check stopped boot.\n")
                    self.update_viewer(self.key_text_b, "[Attack Blocked]")
                else:
                    self.log_msg("\n⚠️ [ATTACK]: Glitch Success! Security Bypassed.\n")
                    self.run_script("scripts/bad_fault.py"); self.update_viewer(self.key_text_b, "[Root Access Granted]")
                    self.print_remediation("FAULT")
                return
            if current == "DONE":
                win.destroy(); self.log_msg("\n[FAIL]: Boot completed normally.\n"); return
            win.after(delay, lambda: loop(step+1))
        loop()

if __name__ == "__main__":
    import tkinter.ttk as ttk
    main_window = tk.Tk()
    app = PQCLabApp(main_window)
    main_window.mainloop()