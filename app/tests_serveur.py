#!/usr/bin/env python3
"""Lance les tests du serveur d'état (serveur/tests, unittest) depuis la
suite du dépôt : `python3 app/tests.py` les voit, et une mutation du
serveur doit les faire tomber."""
import subprocess
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parents[1] / "serveur" / "tests"

if __name__ == "__main__":
    res = subprocess.run([sys.executable, "-W", "ignore", "-m", "unittest", "discover", "-s", str(TESTS), "-q"],
                         capture_output=True, text=True)
    print(res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "")
    if res.returncode:
        print(res.stdout + res.stderr)
    sys.exit(res.returncode)
