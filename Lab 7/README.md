# Lab 7 — Fuzz Testing (Train Fare)

**Student:** Priyanka B M  
**SRN:** PES1UG24AM207  
**Assigned repository:** https://github.com/SETAPESU26/L6_L7_25_train_fare

## Files
- `train_fare.py` — the three assigned functions, hardened against malformed inputs.
- `test_train_fare.py` — Hypothesis fuzz tests and regression tests.
- `requirements.txt` — Hypothesis and pytest dependencies.

## Run
From this directory:

```bash
python3 -m pip install -r requirements.txt
python3 train_fare.py
python3 -m pytest -v test_train_fare.py
```

## Behaviour preserved
- `parse_pnr` returns the zone and remaining PNR number for a 10-digit PNR.
- `journey_distance` returns the last listed distance minus the first.
- `berth_type` preserves the starter's berth table and lookup expression: `BERTHS[int(number) % 8]`.
- Invalid or unsupported inputs return `None` instead of raising an exception, allowing the no-crash fuzz properties to pass.
