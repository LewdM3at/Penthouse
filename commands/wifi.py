"""
actions/wifi.py
All callable actions related to WiFi / 802.11 tooling.

Each function is invoked by TUI._run_action() after curses is suspended,
so stdout/stdin work normally. Print whatever you like.

Convention:
  - Use os.system() for interactive tools that need a full terminal.
  - Use subprocess.run() when you want to capture & display output.
  - Return a truthy value if you want TUI to pause after completion
    so the user can read the output before returning to the menu.
"""

import os
import subprocess
import shlex
import sys


# ─────────────────────────────────────────── helpers ──────────────────

def _iface(prompt="Interface (e.g. wlan0): ", default="wlan0") -> str:
    return input(f"{prompt}[{default}] ") or default


def _run_interactive(cmd: str):
    """Run a command in the current terminal (interactive)."""
    print(f"\n[*] Running: {cmd}\n")
    os.system(cmd)


# ─────────────────────────────────────────── wifite ───────────────────

def wifite_handshake():
    iface = _iface("Monitor interface: ", "wlan0mon")
    _run_interactive(f"wifite --interface {shlex.quote(iface)} --wpa --kill")
    return True


def wifite_wps():
    iface = _iface("Monitor interface: ", "wlan0mon")
    _run_interactive(f"wifite --interface {shlex.quote(iface)} --wps --kill")
    return True


def wifite_pmkid():
    iface = _iface("Monitor interface: ", "wlan0mon")
    _run_interactive(f"wifite --interface {shlex.quote(iface)} --pmkid --kill")
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