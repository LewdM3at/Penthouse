#!/usr/bin/env python3
"""
██████╗ ███████╗███╗   ██╗████████╗██╗  ██╗ ██████╗ ██╗   ██╗███████╗███████╗
██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██║  ██║██╔═══██╗██║   ██║██╔════╝██╔════╝
██████╔╝█████╗  ██╔██╗ ██║   ██║   ███████║██║   ██║██║   ██║███████╗█████╗  
██╔═══╝ ██╔══╝  ██║╚██╗██║   ██║   ██╔══██║██║   ██║██║   ██║╚════██║██╔══╝  
██║     ███████╗██║ ╚████║   ██║   ██║  ██║╚██████╔╝╚██████╔╝███████║███████╗
╚═╝     ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
Pentest Toolkit Launcher — by LewdMeat
"""

import sys
import os

# Ensure the package directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.tui import TUI
from menus.registry import build_menu_tree


def main():
    menu_tree = build_menu_tree()
    app = TUI(menu_tree)
    app.run()


if __name__ == "__main__":
    main()