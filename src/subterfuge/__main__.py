"""Run the installed Subterfuge CLI as a Python module."""
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
