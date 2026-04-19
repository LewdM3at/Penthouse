import os
import subprocess
import shlex
import sys
import subprocess


# ─────────────────────────────────────────── helpers ───────────────────────────

def _clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def _run_interactive(cmd: str):
    """Run a command in the current terminal (interactive)."""
    print(f"\n[*] Running: {cmd}\n")
    os.system(cmd)


# ─────────────────────────────────────────── Chameleon Ultra ───────────────────

def chameleon_start():
    _clear_screen()
    subprocess.Popen(["chameleonultragui"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return False