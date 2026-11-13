"""Run the lab checks from any folder. Optional replay of the original bugs."""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def run(args, folder, expected=0, input_text=None):
    print("\n$ python", " ".join(args), flush=True)
    result = subprocess.run([sys.executable, *args], cwd=folder,
                            input=input_text, text=True)
    if result.returncode != expected:
        raise SystemExit(f"Expected exit {expected}; received {result.returncode}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-original", action="store_true",
                        help="Demonstrate expected failures in a temporary copy")
    args = parser.parse_args()
    lab6, lab7 = ROOT / "Lab 6", ROOT / "Lab 7"
    run(["-m", "coverage", "run", "--source=ski_resort_pass", "-m", "pytest",
         "CodeCoverageTest_ski_resort_pass.py", "-q"], lab6)
    run(["-m", "coverage", "report", "-m", "--fail-under=90"], lab6)
    run(["-m", "coverage", "run", "--branch", "--source=ski_resort_pass", "-m", "pytest",
         "BranchCoverageTest_ski_resort_pass.py", "-q"], lab6)
    run(["-m", "coverage", "report", "-m", "--fail-under=90"], lab6)
    if args.replay_original:
        print("\nORIGINAL BUG REPLAY: the next application and three tests should fail.", flush=True)
        with tempfile.TemporaryDirectory(prefix="ski-resort-original-") as folder:
            path = Path(folder)
            shutil.copy2(lab7 / "evidence" / "processor_original.py", path / "processor.py")
            shutil.copy2(lab7 / "test_processor.py", path / "test_processor.py")
            run(["processor.py"], path, expected=1,
                input_text="2026/12/31\n1:0\nBEG\n")
            run(["-m", "pytest", "test_processor.py", "-k", "no_crash or safe", "-q",
                 "--tb=short"], path, expected=1)
    print("\nFIXED APPLICATION: all tests must pass.", flush=True)
    run(["-m", "pytest", "test_processor.py", "-q"], lab7)
    run(["-m", "pytest", "-q"], ROOT)
    print("\nAll required checks passed.")


if __name__ == "__main__":
    main()
