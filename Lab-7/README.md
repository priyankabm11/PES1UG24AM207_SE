# Lab 7 — Fuzz Testing (Train Fare)

**Student:** Priyanka B M  
**SRN:** PES1UG24AM207  
**Assigned repository:** https://github.com/SETAPESU26/L6_L7_25_train_fare

## Objective
Use Hypothesis property-based fuzzing to uncover malformed-input and edge-case bugs in the three supplied functions, then harden the implementation without changing their public function names or successful return formats.

## Files
- `train_fare.py` — hardened `parse_pnr`, `journey_distance`, and `berth_type` functions, plus an interactive demonstration.
- `test_train_fare.py` — Hypothesis fuzz/property tests and explicit invalid-input regression tests.
- `requirements.txt` — test dependencies.

## Install and run
Run these commands from this directory:

```bash
python -m pip install -r requirements.txt
python train_fare.py
python -m pytest -v test_train_fare.py
```

## Input-validation rules
- `parse_pnr`: accepts exactly 10 ASCII digits and returns `(first_digit, remaining_nine_digits)` as integers.
- `journey_distance`: accepts at least two comma-separated, non-negative integer distances in non-decreasing order; returns last minus first.
- `berth_type`: accepts `COACH-NUMBER`, a coach token with letters optionally followed by digits, and a positive seat number. Berths repeat every eight seats, starting at seat 1 with `SU`.
- Invalid inputs consistently raise a descriptive `ValueError`; the interactive program catches it and continues to the next prompt.

## Testing
The Hypothesis tests generate arbitrary strings and non-string values, then check that inputs either produce a result satisfying the documented property or are rejected with `ValueError`. Additional generated valid-input tests verify the return values. Fixed regression cases cover malformed PNRs, CSV distances, and seat identifiers.

The CI workflow in `.github/workflows/lab7.yml` installs the declared dependencies and runs the same pytest suite on pushes and pull requests.
