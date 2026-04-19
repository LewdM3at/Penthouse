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

def bettercap_start():
    _clear_screen()
    _run_interactive(f'sudo bettercap -eval "ui on" -silent')
    return False



