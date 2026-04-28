import os
import subprocess
import shlex
import sys
import webbrowser
import shutil
import time
import urllib.request


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

    proc = subprocess.Popen(
        ["sudo", "bettercap", "-eval", "ui on", "-silent"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("\n[*] Waiting for Bettercap WebUI to start...")
    for _ in range(20):  # try for up to 10 seconds
        try:
            urllib.request.urlopen("http://localhost:8080", timeout=1)
            break  # server is up
        except Exception:
            time.sleep(0.5)
    else:
        print("\n[!] Bettercap WebUI did not start in time.\n")
        proc.terminate()
        return

    print("\n[*] Opening http://localhost:8080 ...\n")
    opened = webbrowser.open("http://localhost:8080")
    if not opened:
        print("\n[*] Could not open browser. Navigate to: http://localhost:8080\n")

    input("\n[*] Press Enter to stop Bettercap...\n")
    proc.terminate()
    proc.wait()

def bettercap_start():
    _clear_screen()
    _run_interactive(f'sudo bettercap')
    return False



