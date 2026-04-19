import os
import subprocess
import shlex
import sys


# ─────────────────────────────────────────── helpers ──────────────────

def _clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def _iface(prompt="Interface (e.g. wlan0): ", default="wlan0") -> str:
    return input(f"{prompt}[{default}] ") or default

def _pick_wireless_iface() -> str | None:
    """
    Discover wireless interfaces by checking /sys/class/net/<iface>/wireless.
    No external tools needed — reads kernel sysfs directly.
    Returns the chosen interface name, or None if user cancels.
    """
    _clear_screen()
    sys_net = "/sys/class/net"
    wireless = []
 
    for iface in sorted(os.listdir(sys_net)):
        if os.path.isdir(os.path.join(sys_net, iface, "wireless")):
            # Check if it's already in monitor mode by reading operstate / type
            # A monitor interface typically has its name ending in 'mon'
            # or we can read /sys/class/net/<iface>/type — value 801 = monitor
            type_file = os.path.join(sys_net, iface, "type")
            try:
                with open(type_file) as f:
                    iface_type = f.read().strip()
                mode = "monitor" if iface_type == "801" else "managed"
            except OSError:
                mode = "unknown"
            wireless.append((iface, mode))
 
    if not wireless:
        print("\n[!] No wireless interfaces found.\n")
        return None
 
    print("\n  Wireless interfaces:\n")
    for i, (iface, mode) in enumerate(wireless):
        tag = " [monitor]" if mode == "monitor" else ""
        print(f"  [{i}] {iface}{tag}")
 
    print("\n  [q] Cancel\n")
 
    while True:
        choice = input("  Select interface: ").strip().lower()
        if choice == "q":
            return None
        if choice.isdigit() and int(choice) < len(wireless):
            return wireless[int(choice)][0]
        print("  Invalid choice, try again.")


def _run_interactive(cmd: str):
    """Run a command in the current terminal (interactive)."""
    print(f"\n[*] Running: {cmd}\n")
    os.system(cmd)


# ─────────────────────────────────────────── Wifite ───────────────────

def auto_audit():
    _clear_screen()
    _run_interactive(f"sudo wifite --daemon")
    return True

def wifite_handshake():
    _clear_screen()
    _run_interactive(f"sudo wifite --no-pmkid --no-wps --daemon")
    return True

def wifite_pmkid():
    _clear_screen()
    _run_interactive(f"sudo wifite --pmkid --daemon")
    return True

def wifite_pixiedust():
    _clear_screen()
    _run_interactive(f"sudo wifite --pixie --no-pmkid --wps-only --daemon")
    return True

def wifite_pin():
    _clear_screen()
    _run_interactive(f"sudo wifite --no-pixie --no-pmkid --wps-only --daemon")
    return True

# ─────────────────────────────────────────── Kismet ───────────────────

def _kismet_running() -> bool:
    import subprocess
    result = subprocess.run(["pgrep", "-x", "kismet"], capture_output=True)
    return result.returncode == 0

def kismet_status() -> str:
    return "● RUNNING" if _kismet_running() else "○ NOT RUNNING"

def kismet_start_daemon():
    _clear_screen()
    if _kismet_running():
        print("\n[!] Kismet server is already running.\n")
        return True
    iface = _pick_wireless_iface()
    if not iface:
        return True  # just go back to menu
    os.system(f"sudo kismet -c {shlex.quote(iface)} --daemonize")
    return False

def kismet_stop_daemon():
    _clear_screen()
    if not _kismet_running():
        print("\n[!] Kismet server is not running.\n")
        return True
    import signal, time
    print("\n[*] Trying to stop Kismet server with SIGTERM...\n")
    os.system("sudo pkill -TERM -x kismet")
    time.sleep(3)
    if _kismet_running():
        print("\n[*] Trying to stop Kismet server with SIGKILL...\n")
        os.system("sudo pkill -KILL -x kismet")
    return True

def kismet_connect():
    _clear_screen()
    if not _kismet_running():
        print("\n[!] Kismet is not running. Start the server first.\n")
        return True
    import webbrowser, shutil
    print("\n[*] Connecting to Kismet server at http://localhost:2501 ...\n")
    opened = webbrowser.open("http://localhost:2501")
    if not opened:
        print("\n[*] Could not open browser. Navigate to: http://localhost:2501\n")
        return True
    return False

# ─────────────────────────────────────────── Evilginx ─────────────────

def evilginx_start():
    _clear_screen()
    _run_interactive(f"sudo evilginx")
    return True

# ─────────────────────────────────────────── Airgeddon ────────────────

def airgeddon_start():
    _clear_screen()
    _run_interactive(f"sudo airgeddon")
    return True


# ─────────────────────────────────────────── aircrack-ng ──────────────

def airmon_start():
    iface = _iface("Interface to put into monitor mode: ", "wlan0")
    _run_interactive(f"airmon-ng start {shlex.quote(iface)}")
    return True


def airmon_stop():
    iface = _iface("Monitor interface to stop: ", "wlan0mon")
    _run_interactive(f"airmon-ng stop {shlex.quote(iface)}")
    return True


def airodump_scan():
    iface = _iface("Monitor interface: ", "wlan0mon")
    out_prefix = input("Output file prefix (leave empty to skip save): ").strip()
    cmd = f"airodump-ng {shlex.quote(iface)}"
    if out_prefix:
        cmd += f" -w {shlex.quote(out_prefix)}"
    _run_interactive(cmd)
    return True


def aireplay_deauth():
    iface = _iface("Monitor interface: ", "wlan0mon")
    bssid = input("Target BSSID (AP MAC): ").strip()
    count = input("Deauth count [0=infinite]: ").strip() or "0"
    cmd = f"aireplay-ng -0 {shlex.quote(count)} -a {shlex.quote(bssid)} {shlex.quote(iface)}"
    _run_interactive(cmd)
    return True


def aircrack_crack():
    cap_file = input("Path to .cap file: ").strip()
    wordlist = input("Path to wordlist: ").strip()
    _run_interactive(f"aircrack-ng {shlex.quote(cap_file)} -w {shlex.quote(wordlist)}")
    return True


# ─────────────────────────────────────────── misc ─────────────────────

def evil_twin():
    cfg = input("Path to hostapd-wpe config file: ").strip()
    _run_interactive(f"hostapd-wpe {shlex.quote(cfg)}")
    return True


def iwconfig_info():
    _run_interactive("iwconfig 2>/dev/null || ip link")
    return True