# Data

## Source

Nurse Rostering Benchmark Instances 1-24, Tim Curtois (University of Nottingham).

- Page: https://www.schedulingbenchmarks.org/nrp/
- All instances (zip, 576,649 bytes): https://www.schedulingbenchmarks.org/nrp/data/instances1_24.zip
- Single instance: `https://www.schedulingbenchmarks.org/nrp/data/InstanceN.txt` (plain text) or `.ros` (XML)
- Format guide (constraint definitions): https://www.schedulingbenchmarks.org/nrp/instances1_24.html

Checked live on 2026-09-24: no registration needed. Please cite the benchmark page and the reference it lists
(doi 10.1016/j.ejor.2014.01.039) in the report.

## Reproduce

```
conda activate seyon
python src/download_instances.py
```

This fills `data/raw/` (not committed, see `.gitignore`) with `Instance1.txt` ... `Instance24.txt` and the XML versions.

## `best_known.csv`

Instance sizes, best-known lower bound and best-known solution, transcribed from the benchmark page on 2026-09-24.
Used to compute the optimality gap of both methods. For Instances 1-23 the lower bound equals the best-known solution;
Instance 24 has lower bound 40438 and best-known solution 40439.

## Instance file sections

| Section | Meaning |
|---|---|
| `SECTION_HORIZON` | planning horizon in days (day 0 is a Monday) |
| `SECTION_SHIFTS` | shift id, length in minutes, shifts that may not follow it on the next day |
| `SECTION_STAFF` | per nurse: max shifts per type, max/min total minutes, max/min consecutive shifts, min consecutive days off, max weekends |
| `SECTION_DAYS_OFF` | days on which a nurse must not be assigned a shift (hard) |
| `SECTION_SHIFT_ON_REQUESTS` / `SECTION_SHIFT_OFF_REQUESTS` | soft requests with a penalty weight |
| `SECTION_COVER` | required staff per day and shift, with weights for under- and over-cover (soft) |
