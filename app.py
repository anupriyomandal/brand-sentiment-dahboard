"""Root CLI shim that preserves `python app.py` compatibility."""

from cli.app import run


if __name__ == "__main__":
    run()
