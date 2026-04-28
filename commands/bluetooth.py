import os
import subprocess
import shlex
import sys


# ─────────────────────────────────────────── helpers ──────────────────

def _clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def _run_interactive(cmd: str):
    """Run a command in the current terminal (interactive)."""
    print(f"\n[*] Running: {cmd}\n")
    os.system(cmd)


# ─────────────────────────────────────────── Bettercap ────────────────

def bettercap_start_webui():
    _clear_screen()
    _run_interactive(f'sudo bettercap -eval "ui on" -silent')
    import webbrowser, shutil
    print("\n[*] Connecting to Bettercap WebUI at http://localhost:8080 ...\n")
    opened = webbrowser.open("http://localhost:8080")
    if not opened:
        print("\n[*] Could not open browser. Navigate to: http://localhost:8080\n")
        return True
    return False

def bettercap_start():
    _clear_screen()
    _run_interactive(f'sudo bettercap')
    return False



