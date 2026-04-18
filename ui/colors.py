"""
ui/colors.py
Curses color pair definitions and helper lookup.

Color pair IDs are assigned here and referenced by logical name throughout
the rest of the codebase — change them once, applies everywhere.

Terminal palette used (256-colour):
  Background : 232  (near-black)
  Accent     : 46   (bright green  — WiFi)
               208  (orange        — Sub-GHz)
               51   (cyan          — 2.4 GHz / BT)
               201  (magenta       — NFC)
               27   (blue          — Network)
               220  (yellow        — System)
"""

import curses


# ── Pair indices ────────────────────────────────────────────────────── #
_PAIRS: dict = {}
_next_pair_id = 1


def _pair(fg: int, bg: int) -> int:
    global _next_pair_id
    key = (fg, bg)
    if key not in _PAIRS:
        curses.init_pair(_next_pair_id, fg, bg)
        _PAIRS[key] = _next_pair_id
        _next_pair_id += 1
    return curses.color_pair(_PAIRS[key])


# ── Public API ──────────────────────────────────────────────────────── #
_COLOR_MAP: dict = {}


def init_colors():
    """Call once after curses.wrapper() initialises the screen."""
    curses.start_color()
    curses.use_default_colors()

    BG  = 232   # near-black
    BG2 = 234   # slightly lighter panel bg

    _COLOR_MAP.update({
        # Logo
        "logo":            _pair(46,  BG),      # green on black

        # Breadcrumb / nav
        "breadcrumb":      _pair(244, BG),      # grey

        # Dividers
        "divider":         _pair(238, BG),      # dark grey

        # Panel background
        "panel_bg":        _pair(244, BG),

        # Selected item (highlight bar)
        "selected":        _pair(0,   46),      # black on green

        # Category colour tags
        "wifi":            _pair(46,  BG),      # bright green
        "subghz":          _pair(208, BG),      # orange
        "bt":              _pair(51,  BG),      # cyan
        "nfc":             _pair(201, BG),      # magenta
        "net":             _pair(27,  BG),      # blue
        "radio":           _pair(208, BG),      # orange (same as subghz)
        "system":          _pair(220, BG),      # yellow
        "default":         _pair(252, BG),      # near-white

        # Availability
        "unavailable":     _pair(238, BG),      # greyed-out

        # Detail panel
        "description":     _pair(252, BG),
        "requires_header": _pair(244, BG),
        "tool_ok":         _pair(46,  BG),      # green tick
        "tool_missing":    _pair(196, BG),      # red cross

        # Scroll hints
        "scroll_hint":     _pair(240, BG),

        # Status bar
        "status_bar":      _pair(244, BG2),
        "status_count":    _pair(46,  BG2),

        # Dialogs
        "dialog_bg":       _pair(252, 236),
        "dialog_text":     _pair(220, 236),
        "dialog_hint":     _pair(244, 236),
        "error_text":      _pair(196, 236),
    })


def get_color(name: str) -> int:
    """Return the curses attribute for a logical color name."""
    return _COLOR_MAP.get(name, curses.A_NORMAL)