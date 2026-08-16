"""
Root-level launcher for AirWrite Translator.

The actual implementation lives in src/main.py. This file exists only
so the project can be run as `python main.py` from the repository root
without needing to know the internal package layout.
"""

from src.main import run

if __name__ == "__main__":
    run()
