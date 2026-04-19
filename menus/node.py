"""
menus/node.py
Defines the MenuItem and MenuTree data structures.
Each node can be a category (with children) or a leaf (with an action).
"""

from dataclasses import dataclass, field
from typing import Optional, List, Callable


# Color tags map to curses color pair indices (defined in tui.py)
COLOR_WIFI      = "wifi"
COLOR_BLUETOOTH = "bluetooth"
COLOR_SUBGHZ    = "subghz"
COLOR_RADIO     = "radio"
COLOR_NFC       = "nfc"
COLOR_BT        = "bt"
COLOR_NET       = "net"
COLOR_SYSTEM    = "system"
COLOR_DEFAULT   = "default"


@dataclass
class MenuItem:
    """
    A single node in the menu tree.

    Attributes:
        label           : Display name shown in the TUI
        description     : Short description shown in the status bar
        icon            : 1-3 char icon/emoji shown before the label
        color_tag       : Logical color group (maps to a curses color pair)
        children        : Sub-menu items (empty = leaf node)
        action          : Callable executed when a leaf node is selected
        action_args     : Extra keyword arguments forwarded to action()
        confirm         : Whether to ask "Are you sure?" before running
        requires        : List of tool binaries this item needs (e.g. ["aircrack-ng"])
        status_factory  : Optional callable that returns a string to show in the status bar (e.g. to show current interface)
    """
    label: str
    description: str = ""
    icon: str = "›"
    color_tag: str = COLOR_DEFAULT
    children: List["MenuItem"] = field(default_factory=list)
    action: Optional[Callable] = None
    action_args: dict = field(default_factory=dict)
    confirm: bool = False
    requires: List[str] = field(default_factory=list)
    status_factory: Optional[Callable] = None

    # ------------------------------------------------------------------ #
    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def has_action(self) -> bool:
        return self.action is not None

    def execute(self):
        """Run the action associated with this leaf, if any."""
        if self.action:
            return self.action(**self.action_args)
        return None