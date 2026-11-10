"""Preview the splash: python -m exbyte_brand [--tagline TEXT] [--label TEXT]"""

import argparse

from . import DEFAULT_LABEL, DEFAULT_TAGLINE, __version__, play_splash


def main() -> None:
    parser = argparse.ArgumentParser(prog="exbyte-brand", description="Preview the Exbyte splash.")
    parser.add_argument("--tagline", default=DEFAULT_TAGLINE, help="line shown under the logo")
    parser.add_argument("--label", default=DEFAULT_LABEL, help="text shown next to the spinner")
    parser.add_argument("--no-clear", action="store_true", help="do not clear the screen first")
    parser.add_argument("--version", action="version", version=f"exbyte-brand {__version__}")
    args = parser.parse_args()

    play_splash(tagline=args.tagline, label=args.label, clear=not args.no_clear)


if __name__ == "__main__":
    main()
