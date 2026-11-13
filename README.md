# Lab 6 and Lab 7 - Ski Resort Pass

**Name:** Vinayak Yuvraj Kalal  
**SRN:** PES2UG25AM809

## Results

| Lab | Result |
| --- | --- |
| Lab 6 - Line coverage | 14 tests passed; 100% line coverage |
| Lab 6 - Branch coverage | 47 tests passed; 100% branch coverage |
| Lab 7 - Fuzz testing | 44 tests passed after fixing input validation |

## Run

Use Python 3.10 or newer. Open a terminal in this project folder.

```sh
python -m venv .venv
```

Activate the environment using the command for your system:

| System | Command |
| --- | --- |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS/Linux | `source .venv/bin/activate` |

```sh
python -m pip install -r requirements.txt
python run_checks.py
```

If your system uses `python3`, replace `python` with `python3`.

To run the fixed application:

```sh
python "Lab 7/processor.py"
```

Example inputs: `2026/12/31`, `250:1000`, `BEG`.
Expected results: `VALID`, `25.0`, `$35.00`.

## Files

- `Lab 6/`: application, separate line and branch coverage tests, and evidence.
- `Lab 7/`: fixed application, Hypothesis tests, evidence, and the PDF report.
- `run_checks.py`: runs both coverage checks and the Lab 7 tests.

Evidence includes the required terminal screenshots and their recorded output.
The Lab 7 screenshots show the original failures and the passing results after fixes.

## Input validation

| Function | Invalid input result |
| --- | --- |
| `parse_season_pass_validity` | `"INVALID_DATE"` |
| `compute_trail_gradient` | `None` |
| `calculate_lift_access_tier` | `None` |

Dates must be real calendar dates. The lab's validity rule is year >= 2026.
Gradients require finite numbers, drop >= 0, and distance > 0.
Zone prices use the BEG, INT, ADV, and ALL prefixes.
