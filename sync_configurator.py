"""Pull a fresh build of the battery configurator into ./configurator.

The configurator lives in its own project (../ebike-battery-configurator). This runs that
project's web/build_static.py with its own virtual environment and writes the result here, so
the local site matches what GitHub Pages will serve at fryepower.com/configurator/.

    python sync_configurator.py
    python sync_configurator.py --src D:/path/to/ebike-battery-configurator

On GitHub, the configurator repo's publish workflow does the same thing on every push to main,
so running this is only needed for local testing (or to publish by hand).
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_SRC = ROOT.parent / "ebike-battery-configurator"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC, help="configurator project folder")
    args = ap.parse_args()

    src = args.src.resolve()
    build = src / "web" / "build_static.py"
    if not build.exists():
        print(f"Not found: {build}", file=sys.stderr)
        return 1
    venv_py = src / ".venv" / "Scripts" / "python.exe"
    if not venv_py.exists():
        venv_py = src / ".venv" / "bin" / "python"
    python = str(venv_py) if venv_py.exists() else sys.executable

    out = ROOT / "configurator"
    print(f"Building configurator from {src}")
    return subprocess.call([python, str(build), "-o", str(out)], cwd=src)


if __name__ == "__main__":
    sys.exit(main())
