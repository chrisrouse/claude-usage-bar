"""Entry point for `python -m claude_usage_bar` and the installed CLI command."""

import sys
import os

# Support both `python -m claude_usage_bar` (relative) and PyInstaller (absolute)
if __package__:
    from .app import ClaudeUsageApp
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from claude_usage_bar.app import ClaudeUsageApp


def main():
    ClaudeUsageApp().run()


if __name__ == "__main__":
    main()
