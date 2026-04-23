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


# ─────────────────────────────────────────── ProxyChains ────────────────────────

def proxychains_setup():
    _clear_screen()
    home = os.path.expanduser("~")
    proxy_dir = os.path.join(home, ".proxychains")
    proxy_conf = os.path.join(proxy_dir, "proxychains.conf")
    system_conf = "/etc/proxychains.conf"

    # Step 1 — create ~/.proxychains if it doesn't exist
    if not os.path.isdir(proxy_dir):
        os.makedirs(proxy_dir)

    # Step 2 — check system config exists
    if not os.path.isfile(system_conf):
        print("\n[!] /etc/proxychains.conf not found. Is proxychains installed?\n")
        return True

    # Step 3 — copy system config to user dir
    import shutil
    shutil.copy2(system_conf, proxy_conf)
    print(f"\n[*] Copied {system_conf} to {proxy_conf}\n")

    # Step 4 — open with preferred editor
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR") or "nano"
    _run_interactive(f"{shlex.quote(editor)} {shlex.quote(proxy_conf)}")
    return False

# ─────────────────────────────────────────── NMAP ───────────────────────────────

def nmap_start():
    _clear_screen()
    _run_interactive(f"man nmap")
    return False