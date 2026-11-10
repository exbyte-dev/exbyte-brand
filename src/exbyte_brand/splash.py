"""Startup splash animation for the console.

Displays an animated Exbyte.dev branded banner before the main
application starts. Uses ANSI escape codes for color and cursor control.
"""

import os
import re
import shutil
import sys
import time


# ============================================================================
# ANSI escape codes
# ============================================================================

_ESC = "\033["
_RESET = f"{_ESC}0m"
_BOLD = f"{_ESC}1m"
_DIM = f"{_ESC}2m"

_CYAN = f"{_ESC}36m"
_BLUE = f"{_ESC}34m"
_GREEN = f"{_ESC}32m"
_WHITE = f"{_ESC}97m"
_B_CYAN = f"{_ESC}96m"

_CLEAR_SCREEN = f"{_ESC}2J{_ESC}H"
_HIDE_CURSOR = f"{_ESC}?25l"
_SHOW_CURSOR = f"{_ESC}?25h"

_ANSI_RE = re.compile(r"\033\[[0-9;?]*[A-Za-z]")


# ============================================================================
# Logo
# ============================================================================

LOGO_LINES = [
    r"  ______      _           _                _            ",
    r" |  ____|    | |         | |              | |           ",
    r" | |__  __  _| |__  _   _| |_  ___      __| | _____   __",
    r" |  __| \ \/ / '_ \| | | | __|/ _ \    / _` |/ _ \ \ / /",
    r" | |____ >  <| |_) | |_| | |_|  __/ _ | (_| |  __/\ V / ",
    r" |______/_/\_\_.__/ \__, |\__|\___|(_) \__,_|\___| \_/  ",
    r"                     __/ |                               ",
    r"                    |___/                                ",
]

DEFAULT_TAGLINE = "AI | BOTS | AUTOMATION | APIs"
DEFAULT_LABEL = "initializing"


# ============================================================================
# Helpers
# ============================================================================

def _supports_ansi() -> bool:
    """Check if the terminal likely supports ANSI escape codes."""
    if os.getenv("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    if os.getenv("TERM") == "dumb":
        return False
    return True


def _center(text: str, width: int) -> str:
    """Center text within a given width, accounting for visible length."""
    visible = _ANSI_RE.sub("", text)
    pad = max(0, (width - len(visible)) // 2)
    return " " * pad + text


def _write(text: str = "", end: str = "\n") -> None:
    """Write to stdout with flush."""
    sys.stdout.write(text + end)
    sys.stdout.flush()


# ============================================================================
# Animation sequences
# ============================================================================

def _animate_logo(width: int) -> None:
    """Reveal the logo with a top-down sweep effect."""
    for line in LOGO_LINES:
        _write(_center(f"{_B_CYAN}{_BOLD}{line}{_RESET}", width))
        time.sleep(0.04)


def _animate_underline(width: int) -> None:
    """Draw an expanding underline beneath the logo."""
    total = max(len(line) for line in LOGO_LINES)
    bar_char = "─"

    for step in range(1, total + 1, 3):
        centered = _center(f"{_BLUE}{bar_char * step}{_RESET}", width)
        _write(f"\r{centered}", end="")
        time.sleep(0.008)

    _write(f"\r{_center(f'{_BLUE}{bar_char * total}{_RESET}', width)}")


def _animate_tagline(width: int, tagline: str) -> None:
    """Type out the tagline character by character."""
    buffer = ""
    for char in tagline:
        buffer += char
        centered = _center(f"{_DIM}{_WHITE}{buffer}{_RESET}", width)
        _write(f"\r{centered}", end="")
        time.sleep(0.02)
    _write()


def _animate_spinner(width: int, label: str, duration: float) -> None:
    """Show a brief loading spinner."""
    frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.monotonic() + duration
    idx = 0

    while time.monotonic() < end_time:
        frame = frames[idx % len(frames)]
        text = f"{_CYAN}{frame}{_RESET} {_DIM}{label}{_RESET}"
        _write(f"\r{_center(text, width)}", end="")
        time.sleep(0.08)
        idx += 1

    _write(f"\r{' ' * width}\r", end="")


def _show_ready(width: int) -> None:
    """Show the final 'ready' line."""
    _write(_center(f"{_GREEN}{_BOLD}● ready{_RESET}", width))


def _play_plain(tagline: str) -> None:
    """Plain-text fallback for non-ANSI terminals, pipes and log files."""
    for line in LOGO_LINES:
        print(line)
    print()
    if tagline:
        print(f"  {tagline}")
        print()


# ============================================================================
# Public API
# ============================================================================

def play_splash(
    tagline: str = DEFAULT_TAGLINE,
    label: str = DEFAULT_LABEL,
    *,
    clear: bool = True,
    spinner: float = 0.8,
) -> None:
    """Play the startup splash animation.

    Safe to call in any environment. Falls back to a plain-text banner
    when stdout is not a terminal or NO_COLOR is set.

    Args:
        tagline: Line typed out under the logo. Pass "" to skip it.
        label: Text shown next to the spinner.
        clear: Clear the screen before drawing.
        spinner: Spinner duration in seconds. Pass 0 to skip it.
    """
    if not _supports_ansi():
        _play_plain(tagline)
        return

    width = shutil.get_terminal_size((80, 24)).columns

    try:
        _write(_HIDE_CURSOR, end="")
        if clear:
            _write(_CLEAR_SCREEN, end="")

        _write()
        _animate_logo(width)
        _animate_underline(width)
        _write()

        if tagline:
            _animate_tagline(width, tagline)
            _write()

        if spinner > 0:
            _animate_spinner(width, label, spinner)

        _show_ready(width)
        _write()
        time.sleep(0.3)

    except KeyboardInterrupt:
        pass
    finally:
        _write(_SHOW_CURSOR, end="")
