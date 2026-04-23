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
        "logo":            _pair(135,  BG),      # green on black

        # Breadcrumb / nav
        "breadcrumb":      _pair(244, BG),      # grey

        # Dividers
        "divider":         _pair(238, BG),      # dark grey

        # Panel background
        "panel_bg":        _pair(244, BG),

        

        # Category colour tags
        "wifi":                 _pair(120, BG),      # light green
        "selected_wifi":        _pair(0,   46),      # bright green
        "bluetooth":            _pair(45,  BG),      # light blue
        "selected_bluetooth":   _pair(0,   33),      # bright blue
        "rfid":                 _pair(213, BG),      # magenta
        "selected_rfid":        _pair(0,   207),     # bright magenta
        "networking":           _pair(208, BG),      # orange
        "selected_networking":  _pair(0,   202),     # bright orange

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