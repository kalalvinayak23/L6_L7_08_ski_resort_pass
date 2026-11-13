# Lab 6 and Lab 7 - Ski Resort Pass

**Name:** Vinayak Yuvraj Kalal  
**SRN:** PES2UG25AM809  
**GitHub:** kalalvinayak23

Assigned starter: https://github.com/SETAPESU26/L6_L7_08_ski_resort_pass

## Results

| Check | Verified result |
| --- | --- |
| Lab 6 line test suite | 14 tests passed; 59/59 statements covered (100%) |
| Lab 6 branch test suite | 47 tests passed; 42/42 branch exits covered (100%) |
| Lab 7 original fuzz checks | All three failed; Hypothesis reduced the failures to `None` |
| Lab 7 fixed test suite | 44 tests passed |

Lab 6 application logic is unchanged. The two required test files are separate.
The original starter test is also retained.

## Run in simple steps

1. Install Python 3.10 or newer. Verification used Python 3.12.14.
2. Download and extract this project, or clone your submitted repository.
3. Open a terminal in the project folder (the folder containing this README).
4. Create a virtual environment: `python -m venv .venv`.
5. Activate it:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - Windows Command Prompt: `.venv\Scripts\activate.bat`
   - macOS/Linux: `source .venv/bin/activate`
6. Install the packages: `python -m pip install -r requirements.txt`.
7. Run all checks: `python run_checks.py`.
8. To also demonstrate the original failures safely, run
   `python run_checks.py --replay-original`.

If your computer uses `python3`, use `python3` instead of `python`.
During original replay, a crashed application and three failing tests are expected.
The script then verifies the fixed application. It leaves the fixed file in place.

To try the fixed application yourself: `python "Lab 7/processor.py"`.
Enter `2026/12/31`, `250:1000`, and `BEG` at the three prompts.
Expected values: VALID, 25.0, and $35.00.
Try `bad`, `1:0`, and `XYZ` to see the validation messages without a crash.

## Lab 6 commands

Run these inside the `Lab 6` folder:

```sh
python -m coverage run --source=ski_resort_pass -m pytest CodeCoverageTest_ski_resort_pass.py -q
python -m coverage report -m --fail-under=90
python -m coverage run --branch --source=ski_resort_pass -m pytest BranchCoverageTest_ski_resort_pass.py -q
python -m coverage report -m --fail-under=90
```

The branch-mode report's Cover column combines statements and branches.
`evidence/branch_coverage.json` separately confirms 42 covered and zero missing branches.
Coverage describes executed code and branch exits; it does not prove every possible path or input is correct.

## Lab 7 behavior and fixes

| Function | Accepted input | Invalid result |
| --- | --- | --- |
| `parse_season_pass_validity` | Real ASCII calendar dates such as `2028/02/29`; surrounding whitespace is accepted | `"INVALID_DATE"` |
| `compute_trail_gradient` | Two finite numbers as `drop:distance`, with drop >= 0 and distance > 0 | `None` |
| `calculate_lift_access_tier` | Case-insensitive BEG, INT, ADV, ALL prefixes, with whitespace allowed | `None` |

The date uses the starter's **year >= 2026** rule. It does not compare with today's date.
Calendar validation now rejects impossible dates such as `2026/02/30`.
The original three-character zone prefix rule remains: `beginner` maps to BEG.
Gradient validation rejects division by zero, negative dimensions, NaN, infinity,
and nonfinite results caused by overflow. Date and gradient input lengths are bounded.
All three functions safely reject non-string input, including None.

The three robustness properties each generated 500 passing examples after the fix.
Further properties exercised 300 real dates, 500 valid gradients, and all 32
zone/case/whitespace combinations: **2,332 passing generated examples** in the recorded run,
plus ordinary regression cases. Hypothesis "invalid test cases" in statistics mean
discarded generator attempts, not failed application tests.

## Evidence

- `Lab 6/evidence/`: the two required coverage screenshots, raw outputs, and JSON reports.
- `Lab 7/evidence/`: original crash, original failing fuzz tests, fixed CLI,
  passing tests, full Hypothesis statistics, and the original processor for replay.
- `Lab 7/PES2UG25AM809_Lab6_Lab7_Report.pdf`: the screenshot report for submission.

Screenshots show recorded command output displayed in a real terminal.
Full, unabridged output is retained in the accompanying text logs.
The original failure screenshot shows the last 24 lines of its full log.

## Viva reminders

- Line coverage asks whether each executable line ran.
- Branch coverage asks whether every decision exit ran.
- Hypothesis generates inputs and shrinks a failure to a smaller example.
- `None` broke all three original functions because they called string methods on it.
- Explicit input checks and safe invalid results keep the fixed program running.
- Ordinary assertions check correct answers as well as absence of crashes.
