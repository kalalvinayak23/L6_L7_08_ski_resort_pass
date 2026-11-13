"""Run Lab 6 coverage checks and Lab 7 tests."""
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run(args, folder):
    print("\n$ python", shlex.join(args), flush=True)
    subprocess.run([sys.executable, *args], cwd=folder, check=True)


def main():
    lab6 = ROOT / "Lab 6"
    for test_file, branch in [
        ("CodeCoverageTest_ski_resort_pass.py", False),
        ("BranchCoverageTest_ski_resort_pass.py", True),
    ]:
        args = ["-m", "coverage", "run", "--source=ski_resort_pass"]
        if branch:
            args.append("--branch")
        run([*args, "-m", "pytest", test_file, "-q"], lab6)
        run(["-m", "coverage", "report", "-m", "--fail-under=90"], lab6)
    run(["-m", "pytest", "test_processor.py", "-q"], ROOT / "Lab 7")
    print("\nAll lab checks passed.")


if __name__ == "__main__":
    main()
