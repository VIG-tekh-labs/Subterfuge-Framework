#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subterfuge.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
# Maintenance checkpoint: 2026-10-08; legacy runtime migration pending.
