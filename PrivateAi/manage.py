#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

if os.environ.get("RUN_MAIN") == "true":
    try:
        import pydevd_pycharm

        pydevd_pycharm.settrace('host.docker.internal', port=5678, suspend=False)
    except ConnectionRefusedError:
        print("PyCharm debugger not available, continuing without it.")

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PrivateAi.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
