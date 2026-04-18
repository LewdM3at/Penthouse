"""
ui/input_dialog.py
Small helper to prompt the user for text input inside a curses dialog box.
Used by actions that need a target IP, interface name, file path, etc.
"""

import curses
from ui.colors import get_color


def prompt_input(stdscr, prompt: str, default: str = "") -> str:
    """
    Show a centred input dialog and return the entered string.
    Returns `default` if the user cancels with Esc.
    """
    curses.echo()
    curses.curs_set(1)

    h_screen, w_screen = stdscr.getmaxyx()
    dialog_w = min(70, w_screen - 4)
    dialog_h = 5
    dy = (h_screen - dialog_h) // 2
    dx = (w_screen - dialog_w) // 2

    win = curses.newwin(dialog_h, dialog_w, dy, dx)
    win.bkgd(" ", get_color("dialog_bg"))
    win.border()

    label = prompt[:dialog_w - 4]
    win.addstr(1, 2, label, get_color("dialog_text") | curses.A_BOLD)

    # Input field
    field_x = 2
    field_y = 3
    field_w = dialog_w - 4
    win.addstr(field_y, field_x, " " * field_w, get_color("dialog_bg") | curses.A_REVERSE)
    win.addstr(field_y, field_x, default, get_color("dialog_bg") | curses.A_REVERSE)
    win.refresh()

    # Read characters manually so we can handle Esc
    buf = list(default)
    win.move(field_y, field_x + len(buf))

    result = default
    try:
        while True:
            ch = win.getch()
            if ch in (10, 13, curses.KEY_ENTER):           # Enter
                result = "".join(buf)
                break
            elif ch == 27:                                  # Esc → cancel
                result = default
                break
            elif ch in (curses.KEY_BACKSPACE, 127, 8):     # Backspace
                if buf:
                    buf.pop()
            elif 32 <= ch <= 126:                           # Printable
                if len(buf) < field_w - 1:
                    buf.append(chr(ch))
            # Redraw field
            display = "".join(buf)[:field_w]
            win.addstr(field_y, field_x, display.ljust(field_w), get_color("dialog_bg") | curses.A_REVERSE)
            win.move(field_y, field_x + len(buf))
            win.refresh()
    finally:
        curses.noecho()
        curses.curs_set(0)

    return result