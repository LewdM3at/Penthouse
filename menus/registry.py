"""
menus/registry.py
Central place where every menu item is declared.
Add / remove / reorder items here to customise the launcher.

Structure:
    build_menu_tree() -> List[MenuItem]   (top-level items)

Each top-level item can nest children arbitrarily deep.
Leaf nodes carry an `action` callable from the actions package.
"""

from menus.node import (
    MenuItem,
    COLOR_WIFI, COLOR_SUBGHZ, COLOR_RADIO,
    COLOR_NFC, COLOR_BT, COLOR_NET, COLOR_SYSTEM, COLOR_DEFAULT,
)
import commands.wifi     as wifi_commands
#import commands.radio    as radio_commands
#import commands.nfc      as nfc_commands
#import commands.network  as net_commands
#import commands.system   as sys_commands


# ═══════════════════════════════════════════════════════════════════════ #
#  WIFI
# ═══════════════════════════════════════════════════════════════════════ #
def _wifi_menu() -> MenuItem:
    return MenuItem(
        label="  Wi-Fi",
        description="802.11 wireless attack & analysis tools",
        icon="▸",
        color_tag=COLOR_WIFI,
        children=[
            MenuItem(
                label="Wifite",
                description="Automated wireless auditor",
                icon=" ",
                color_tag=COLOR_WIFI,
                children=[
                    MenuItem(
                        label="Automated Audit",
                        description="Run automated wireless audit (sudo wifite --daemon)",
                        icon="󱜙 ",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.auto_audit,
                        requires=["wifite"],
                        confirm=True,
                    ),
                    MenuItem(
                        label="Handshake Capture",
                        description="Capture WPA/WPA2 handshakes (sudo wifite --no-pmkid --no-wps --daemon)",
                        icon=" ",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.wifite_handshake,
                        requires=["wifite"],
                        confirm=True,
                    ),
                    MenuItem(
                        label="PMKID Attack",
                        description="Clientless PMKID hash capture (sudo wifite --pmkid --daemon)",
                        icon=" ",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.wifite_pmkid,
                        requires=["wifite"],
                        confirm=True,
                    ),
                    MenuItem(
                        label="PixieDust Attack",
                        description="Attack WPS-enabled routers (sudo wifite --pixie --no-pmkid --wps-only --daemon)",
                        icon="󱊨 ",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.wifite_pixiedust,
                        requires=["wifite"],
                        confirm=True,
                    ),
                    MenuItem(
                        label="PIN Attack",
                        description="Attack WPS-enabled routers (sudo wifite --no-pixie --no-pmkid --wps-only --daemon)",
                        icon="󰐃 ",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.wifite_pin,
                        requires=["wifite"],
                        confirm=True,
                    ),
                ],
            ),
            MenuItem(
                label="Aircrack-ng Suite",
                description="Classic 802.11 toolkit",
                icon=" ",
                color_tag=COLOR_WIFI,
                children=[
                    MenuItem(
                        label="Monitor Mode ON",
                        description="Put interface into monitor mode (airmon-ng start)",
                        icon="📡",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.airmon_start,
                        requires=["airmon-ng"],
                    ),
                    MenuItem(
                        label="Monitor Mode OFF",
                        description="Stop monitor mode (airmon-ng stop)",
                        icon="🔇",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.airmon_stop,
                        requires=["airmon-ng"],
                    ),
                    MenuItem(
                        label="Scan Networks",
                        description="Passive scan with airodump-ng",
                        icon="🔍",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.airodump_scan,
                        requires=["airodump-ng"],
                    ),
                    MenuItem(
                        label="Deauth Attack",
                        description="Send deauth frames (aireplay-ng -0)",
                        icon="💣",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.aireplay_deauth,
                        requires=["aireplay-ng"],
                        confirm=True,
                    ),
                    MenuItem(
                        label="Crack Handshake",
                        description="Dictionary attack on .cap file (aircrack-ng)",
                        icon="🔓",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.aircrack_crack,
                        requires=["aircrack-ng"],
                    ),
                ],
            ),
            MenuItem(
                label="Hostapd Evil Twin",
                description="Create a rogue AP with hostapd-wpe",
                icon="👹",
                color_tag=COLOR_WIFI,
                action=wifi_commands.evil_twin,
                requires=["hostapd-wpe"],
                confirm=True,
            ),
            MenuItem(
                label="WiFi Info (iwconfig)",
                description="Show current wireless interface info",
                icon="ℹ",
                color_tag=COLOR_WIFI,
                action=wifi_commands.iwconfig_info,
            ),
        ],
    )



# ═══════════════════════════════════════════════════════════════════════ #
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════ #
def build_menu_tree():
    """Return the ordered list of top-level menu items."""
    return [
        _wifi_menu()
        #_subghz_menu(),
        #_24ghz_menu(),
        #_nfc_menu(),
        #_network_menu(),
        #_system_menu(),
    ]