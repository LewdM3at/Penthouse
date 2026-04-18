"""
ui/tui.py
Curses-based terminal UI engine.

Layout:
  ┌─────────────────────────────────────────────┐
  │  HEADER  (logo + breadcrumb)                │
  ├──────────────────┬──────────────────────────┤
  │  MENU LIST       │  DETAIL PANEL            │
  │  (left column)   │  (right column)          │
  │                  │                          │
  ├──────────────────┴──────────────────────────┤
  │  STATUS BAR  (keys + description)           │
  └─────────────────────────────────────────────┘

Key bindings:
  ↑/↓ or k/j   Navigate
  Enter/→/l     Select / enter submenu
  Esc/←/h/q     Back / quit
  r             Re-check tool availability
"""

import curses
import curses.ascii
import os
import shutil
from typing import List, Optional

from menus.node import MenuItem
from ui.colors import init_colors, get_color
from ui.input_dialog import prompt_input


LOGO_LINES = [
    " ██████╗ ███████╗███╗   ██╗████████╗██╗  ██╗ ██████╗ ██╗   ██╗███████╗███████╗",
    " ██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██║  ██║██╔═══██╗██║   ██║██╔════╝██╔════╝",
    " ██████╔╝█████╗  ██╔██╗ ██║   ██║   ███████║██║   ██║██║   ██║███████╗█████╗  ",
    " ██╔═══╝ ██╔══╝  ██║╚██╗██║   ██║   ██╔══██║██║   ██║██║   ██║╚════██║██╔══╝  ",
    " ██║     ███████╗██║ ╚████║   ██║   ██║  ██║╚██████╔╝╚██████╔╝███████║███████╗",
    " ╚═╝     ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝",
]
LOGO_HEIGHT = len(LOGO_LINES)
LOGO_WIDTH  = max(len(l) for l in LOGO_LINES)
HEADER_HEIGHT = LOGO_HEIGHT + 3   # 1 top padding + logo + breadcrumb + divider
STATUS_HEIGHT = 3
LEFT_WIDTH_RATIO = 0.42            # fraction of screen width for menu list


class TUI:
    def __init__(self, menu_tree: List[MenuItem]):
        self.root_items = menu_tree
        # Navigation stack: list of (items_list, selected_index)
        self.nav_stack: List[tuple] = []
        self.current_items: List[MenuItem] = menu_tree
        self.selected: int = 0
        self.scroll_offset: int = 0
        self.stdscr = None
        self.h = self.w = 0
        self.left_w = 0
        self.list_h = 0
        self._tool_cache: dict = {}   # item label -> bool (tool present?)
        self._message: Optional[str] = None  # transient status message

    # ================================================================== #
    #  Entry point
    # ================================================================== #
    def run(self):
        curses.wrapper(self._main)

    def _main(self, stdscr):
        self.stdscr = stdscr
        init_colors()
        curses.curs_set(0)
        stdscr.keypad(True)

        self._recalc_dims()
        self._refresh_tool_cache()

        while True:
            self._draw()
            key = stdscr.getch()
            if not self._handle_key(key):
                break

    # ================================================================== #
    #  Dimensions
    # ================================================================== #
    def _recalc_dims(self):
        self.h, self.w = self.stdscr.getmaxyx()
        self.left_w = max(28, int(self.w * LEFT_WIDTH_RATIO))
        self.list_h = self.h - HEADER_HEIGHT - STATUS_HEIGHT

    # ================================================================== #
    #  Key handling
    # ================================================================== #
    def _handle_key(self, key) -> bool:
        """Return False to quit."""
        items = self.current_items

        # Movement
        if key in (curses.KEY_UP, ord('k')):
            self.selected = max(0, self.selected - 1)
            self._clamp_scroll()

        elif key in (curses.KEY_DOWN, ord('j')):
            self.selected = min(len(items) - 1, self.selected + 1)
            self._clamp_scroll()

        # Enter submenu or run action
        elif key in (curses.KEY_ENTER, 10, 13, curses.KEY_RIGHT, ord('l')):
            if items:
                item = items[self.selected]
                if not item.is_leaf:
                    self.nav_stack.append((self.current_items, self.selected, self.scroll_offset))
                    self.current_items = item.children
                    self.selected = 0
                    self.scroll_offset = 0
                else:
                    self._run_action(item)

        # Back
        elif key in (curses.KEY_BACKSPACE, curses.KEY_LEFT, 27,
                     ord('h'), ord('b')):
            if self.nav_stack:
                self.current_items, self.selected, self.scroll_offset = self.nav_stack.pop()
            else:
                return self._confirm_quit()

        # Quit from root
        elif key in (ord('q'), ord('Q')):
            return self._confirm_quit()

        # Refresh tool cache
        elif key == ord('r'):
            self._refresh_tool_cache()
            self._message = " Tool check refreshed."

        return True

    def _confirm_quit(self) -> bool:
        ans = self._yes_no_dialog("Quit Penthouse?")
        return not ans

    # ================================================================== #
    #  Scroll clamping
    # ================================================================== #
    def _clamp_scroll(self):
        visible = self.list_h - 2
        if self.selected < self.scroll_offset:
            self.scroll_offset = self.selected
        elif self.selected >= self.scroll_offset + visible:
            self.scroll_offset = self.selected - visible + 1

    # ================================================================== #
    #  Tool availability
    # ================================================================== #
    def _refresh_tool_cache(self):
        for item in self._iter_all(self.root_items):
            for tool in item.requires:
                self._tool_cache[tool] = shutil.which(tool) is not None

    def _item_available(self, item: MenuItem) -> bool:
        return all(self._tool_cache.get(t, False) for t in item.requires)

    @staticmethod
    def _iter_all(items):
        for it in items:
            yield it
            if it.children:
                yield from TUI._iter_all(it.children)

    # ================================================================== #
    #  Action execution
    # ================================================================== #
    def _run_action(self, item: MenuItem):
        if item.requires and not self._item_available(item):
            missing = [t for t in item.requires if not self._tool_cache.get(t, False)]
            self._alert_dialog(f"Missing tools: {', '.join(missing)}")
            return

        if item.confirm:
            if not self._yes_no_dialog(f"Run: {item.label}?"):
                return

        # Suspend curses, run action in terminal, restore
        curses.def_prog_mode()
        curses.endwin()
        try:
            result = item.execute()
            if result:
                input(f"\n[Done] Press Enter to return to Penthouse…")
        except Exception as exc:
            print(f"\n[ERROR] {exc}")
            input("Press Enter to return to Penthouse…")
        finally:
            curses.reset_prog_mode()
            self.stdscr.refresh()
            self._refresh_tool_cache()

    # ================================================================== #
    #  Drawing
    # ================================================================== #
    def _draw(self):
        self._recalc_dims()
        s = self.stdscr
        s.erase()

        self._draw_header()
        self._draw_menu_list()
        self._draw_detail_panel()
        self._draw_status_bar()

        s.refresh()

    # ── Header ─────────────────────────────────────────────────────────
    def _draw_header(self):
        s = self.stdscr
        bg        = get_color("panel_bg")
        logo_color = get_color("logo")

        # ── Fill the entire screen with the background color first ──────
        # Curses only paints cells that receive a character; anything not
        # explicitly written keeps the terminal's default background.
        # Stamping a space with our color pair on every cell fixes that.
        for row in range(self.h):
            try:
                s.addstr(row, 0, " " * self.w, bg)
            except curses.error:
                pass   # bottom-right cell always raises — safe to ignore

        # ── Row 0: empty top padding ─────────────────────────────────────
        # (already filled with bg above, nothing extra needed)

        # ── Rows 1‥LOGO_HEIGHT: centered logo ───────────────────────────
        logo_x = max(0, (self.w - LOGO_WIDTH) // 2)
        for i, line in enumerate(LOGO_LINES):
            row = i + 1          # +1 for the top padding row
            if row >= self.h:
                break
            try:
                s.addstr(row, logo_x, line[:self.w - logo_x], logo_color | curses.A_BOLD)
            except curses.error:
                pass

        # ── Breadcrumb ───────────────────────────────────────────────────
        bc_y = LOGO_HEIGHT + 2   # logo rows (1‥LOGO_HEIGHT) + 2 padding row
        breadcrumb = self._breadcrumb()
        try:
            s.addstr(bc_y, 0, (" " + breadcrumb)[:self.w], get_color("breadcrumb"))
        except curses.error:
            pass

        # ── Horizontal divider ───────────────────────────────────────────
        div_y = bc_y + 1
        try:
            s.addstr(div_y, 0, "─" * self.w, get_color("divider"))
        except curses.error:
            pass

    def _breadcrumb(self) -> str:
        parts = ["HOME"]
        for items, idx, _ in self.nav_stack:
            parts.append(items[idx].label)
        if self.nav_stack:
            parts.append("…")
        return " › ".join(parts)

    # ── Menu list (left panel) ─────────────────────────────────────────
    def _draw_menu_list(self):
        s = self.stdscr
        items = self.current_items
        panel_y = HEADER_HEIGHT
        panel_x = 0
        visible = self.list_h - 2  # leave room for scroll indicators

        # Panel border / background
        for row in range(self.list_h):
            try:
                s.addstr(panel_y + row, 0, " " * self.left_w, get_color("panel_bg"))
            except curses.error:
                pass

        # Scroll up indicator
        if self.scroll_offset > 0:
            try:
                s.addstr(panel_y, 2, "  ▲  more  ▲  ", get_color("scroll_hint"))
            except curses.error:
                pass

        for i in range(visible):
            idx = i + self.scroll_offset
            if idx >= len(items):
                break
            item = items[idx]
            row = panel_y + i + 1
            is_selected = (idx == self.selected)
            avail = self._item_available(item)

            self._draw_menu_item(row, panel_x, item, is_selected, avail)

        # Scroll down indicator
        if self.scroll_offset + visible < len(items):
            try:
                s.addstr(panel_y + visible + 1, 2, "  ▼  more  ▼  ", get_color("scroll_hint"))
            except curses.error:
                pass

        # Vertical divider
        for row in range(self.list_h):
            try:
                s.addstr(panel_y + row, self.left_w, "│", get_color("divider"))
            except curses.error:
                pass

    def _draw_menu_item(self, row, x, item: MenuItem, selected: bool, available: bool):
        s = self.stdscr
        max_label = self.left_w - 6  # icon(2) + spaces + arrow

        label = item.label[:max_label]
        arrow = " ›" if not item.is_leaf else "  "
        unavail_marker = " ✗" if item.is_leaf and not available else "  "

        if selected:
            base_attr = get_color("selected") | curses.A_BOLD | curses.A_REVERSE
        else:
            base_attr = get_color(item.color_tag)
            if not available and item.is_leaf:
                base_attr = get_color("unavailable")

        line = f" {item.icon} {label}{unavail_marker}{arrow} "
        line = line[:self.left_w]

        try:
            s.addstr(row, x, line.ljust(self.left_w), base_attr)
        except curses.error:
            pass

    # ── Detail panel (right) ───────────────────────────────────────────
    def _draw_detail_panel(self):
        s = self.stdscr
        panel_y = HEADER_HEIGHT
        panel_x = self.left_w + 1
        panel_w = self.w - self.left_w - 1
        if panel_w < 5:
            return

        items = self.current_items
        if not items:
            return
        item = items[self.selected]

        # Blank panel
        for row in range(self.list_h):
            try:
                s.addstr(panel_y + row, panel_x, " " * panel_w, get_color("panel_bg"))
            except curses.error:
                pass

        row = panel_y + 1

        # Title
        title = f" {item.icon}  {item.label} "
        try:
            s.addstr(row, panel_x + 1, title[:panel_w - 2], get_color(item.color_tag) | curses.A_BOLD)
        except curses.error:
            pass
        row += 1

        # Divider
        try:
            s.addstr(row, panel_x + 1, "─" * (panel_w - 2), get_color("divider"))
        except curses.error:
            pass
        row += 2

        # Description (word-wrapped)
        desc = item.description
        if desc:
            for line in self._wrap(desc, panel_w - 4):
                try:
                    s.addstr(row, panel_x + 2, line, get_color("description"))
                except curses.error:
                    pass
                row += 1
            row += 1

        # Required tools
        if item.requires:
            try:
                s.addstr(row, panel_x + 2, "Requires:", get_color("requires_header") | curses.A_BOLD)
            except curses.error:
                pass
            row += 1
            for tool in item.requires:
                ok = self._tool_cache.get(tool, False)
                mark = "✔" if ok else "✘"
                color = get_color("tool_ok") if ok else get_color("tool_missing")
                try:
                    s.addstr(row, panel_x + 3, f"{mark} {tool}", color)
                except curses.error:
                    pass
                row += 1
            row += 1

        # Children preview
        if item.children:
            try:
                s.addstr(row, panel_x + 2, f"Sub-items ({len(item.children)}):", get_color("requires_header") | curses.A_BOLD)
            except curses.error:
                pass
            row += 1
            for child in item.children[:6]:
                try:
                    s.addstr(row, panel_x + 3, f"› {child.label}"[:panel_w - 5], get_color("description"))
                except curses.error:
                    pass
                row += 1
                if row >= panel_y + self.list_h - 1:
                    break
            if len(item.children) > 6:
                try:
                    s.addstr(row, panel_x + 3, f"  … +{len(item.children) - 6} more", get_color("scroll_hint"))
                except curses.error:
                    pass

    # ── Status bar ─────────────────────────────────────────────────────
    def _draw_status_bar(self):
        s = self.stdscr
        bar_y = self.h - STATUS_HEIGHT

        try:
            s.addstr(bar_y, 0, "─" * self.w, get_color("divider"))
        except curses.error:
            pass

        keys = " ↑↓ Navigate   Enter/→ Select   ← Back   r Recheck tools   q Quit "
        if self._message:
            keys = self._message
            self._message = None

        try:
            s.addstr(bar_y + 1, 0, keys[:self.w].ljust(self.w), get_color("status_bar"))
        except curses.error:
            pass

        # Right-aligned item count
        count_str = f" {self.selected + 1}/{len(self.current_items)} "
        cx = self.w - len(count_str) - 1
        try:
            s.addstr(bar_y + 1, cx, count_str, get_color("status_count") | curses.A_BOLD)
        except curses.error:
            pass

    # ================================================================== #
    #  Dialogs
    # ================================================================== #
    def _yes_no_dialog(self, question: str) -> bool:
        """Centered yes/no dialog. Returns True for yes."""
        h, w = 5, min(60, self.w - 4)
        y = (self.h - h) // 2
        x = (self.w - w) // 2
        win = curses.newwin(h, w, y, x)
        win.bkgd(" ", get_color("dialog_bg"))
        win.border()
        q = question[:w - 4]
        win.addstr(1, (w - len(q)) // 2, q, get_color("dialog_text") | curses.A_BOLD)
        hint = "  [Y]es  /  [N]o  "
        win.addstr(3, (w - len(hint)) // 2, hint, get_color("dialog_hint"))
        win.refresh()
        while True:
            k = win.getch()
            if k in (ord('y'), ord('Y')):
                return True
            if k in (ord('n'), ord('N'), 27, ord('q')):
                return False

    def _alert_dialog(self, message: str):
        """Centered alert box."""
        h, w = 5, min(len(message) + 6, self.w - 4)
        y = (self.h - h) // 2
        x = (self.w - w) // 2
        win = curses.newwin(h, w, y, x)
        win.bkgd(" ", get_color("dialog_bg"))
        win.border()
        msg = message[:w - 4]
        win.addstr(1, (w - len(msg)) // 2, msg, get_color("error_text") | curses.A_BOLD)
        hint = "  Press any key  "
        win.addstr(3, (w - len(hint)) // 2, hint, get_color("dialog_hint"))
        win.refresh()
        win.getch()

    # ================================================================== #
    #  Helpers
    # ================================================================== #
    @staticmethod
    def _wrap(text: str, width: int) -> List[str]:
        words = text.split()
        lines = []
        current = ""
        for word in words:
            if len(current) + len(word) + 1 <= width:
                current = (current + " " + word).strip()
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [""]