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
    COLOR_WIFI, COLOR_BLUETOOTH, COLOR_SUBGHZ, COLOR_RADIO,
    COLOR_NFC, COLOR_BT, COLOR_NET, COLOR_SYSTEM, COLOR_DEFAULT,
)
import commands.wifi     as wifi_commands
#import commands.bluetooth as bt_commands
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
                icon="󰭥 ",
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
                label="Kismet",
                description="Kismet is a sniffer, WIDS, and wardriving tool for Wi-Fi, Bluetooth, Zigbee, RF, and more, which runs on Linux and macOS.",
                icon=" ",
                color_tag=COLOR_WIFI,
                status_factory=wifi_commands.kismet_status,
                children=[
                    MenuItem(
                        label="Start Kismet Server",
                        description="Start the Kismet server",
                        icon="⏻ ",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.kismet_start_daemon,
                        requires=["kismet"],
                    ),
                    MenuItem(
                        label="Stop Kismet Server",
                        description="Stop the Kismet server",
                        icon="⭘ ",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.kismet_stop_daemon,
                        requires=["kismet"],
                    ),
                    MenuItem(
                        label="Connect to Kismet Server",
                        description="Connect to the running Kismet server",
                        icon=" ",
                        color_tag=COLOR_WIFI,
                        action=wifi_commands.kismet_connect,
                        requires=["kismet"],
                    ),
                ],
            ),
            MenuItem(
                label="Evilginx",
                description="Evilginx is a man-in-the-middle attack framework used for phishing login credentials along with session cookies, which in turn allows to bypass 2-factor authentication protection.",
                icon="󱚝 ",
                color_tag=COLOR_WIFI,
                action=wifi_commands.evilginx_start,
                requires=["evilginx"],
                confirm=True,
            ),
            MenuItem(
                label="Airgeddon",
                description="This is a multi-use bash script for Linux systems to audit wireless networks.",
                icon=" ",
                color_tag=COLOR_WIFI,
                action=wifi_commands.airgeddon_start,
                requires=["airgeddon"],
                confirm=True,
            ),
        ],
    )

# ═══════════════════════════════════════════════════════════════════════ #
#  Bluetooth
# ═══════════════════════════════════════════════════════════════════════ #
def _bluetooth_menu() -> MenuItem:
    return MenuItem(
        label="󰂯  Bluetooth",
        description="Bluetooth attack & analysis tools",
        icon="▸",
        color_tag=COLOR_BLUETOOTH,
        children=[
            MenuItem(
                label="BlueZ",
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
                ],
            ),
        ],
    )

# ═══════════════════════════════════════════════════════════════════════ #
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════ #
def build_menu_tree():
    """Return the ordered list of top-level menu items."""
    return [
        _wifi_menu(),
        _bluetooth_menu(),
        #_subghz_menu(),
        #_24ghz_menu(),
        #_nfc_menu(),
        #_network_menu(),
        #_system_menu(),
    ]