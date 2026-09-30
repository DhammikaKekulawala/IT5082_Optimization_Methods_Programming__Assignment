"""Shared code for the Nurse/Staff Rostering assignment.

Imported by both notebooks (01_ilp.ipynb, 02_ga.ipynb, 03_comparison.ipynb) so the
instance format is parsed identically everywhere and only lives in one place.

File format: Nurse Rostering Benchmark Instances 1-24 (Curtois & Qu), see data/README.md
and https://www.schedulingbenchmarks.org/nrp/instances1_24.html
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


@dataclass
class Instance:
    """One parsed benchmark instance."""

    name: str
    n_days: int

    # Shifts, in the order they appear in SECTION_SHIFTS.
    shift_ids: List[str]
    shift_len: Dict[str, int]                       # shift_id -> length in minutes
    forbidden_next: Dict[str, Set[str]]              # shift_id -> shifts that must not follow it next day

    # Staff, in the order they appear in SECTION_STAFF.
    nurse_ids: List[str]
    max_shifts: Dict[str, Dict[str, int]]            # nurse -> shift_id -> max count over the horizon
    max_minutes: Dict[str, int]                      # nurse -> max total minutes
    min_minutes: Dict[str, int]                      # nurse -> min total minutes
    max_consec: Dict[str, int]                       # nurse -> max consecutive working days
    min_consec: Dict[str, int]                       # nurse -> min consecutive working days (once a block starts)
    min_days_off: Dict[str, int]                     # nurse -> min consecutive days off (once a block starts)
    max_weekends: Dict[str, int]                     # nurse -> max weekends worked over the horizon

    # Fixed days off: nurse -> set of day indexes (0-based, day 0 is a Monday).
    days_off: Dict[str, Set[int]]

    # Soft requests: each entry is (nurse, day, shift_id, weight).
    on_requests: List[Tuple[str, int, str, int]]
    off_requests: List[Tuple[str, int, str, int]]

    # Cover requirement: (day, shift_id) -> (required, weight_under, weight_over).
    cover: Dict[Tuple[int, str], Tuple[int, int, int]]

    @property
    def n_nurses(self) -> int:
        return len(self.nurse_ids)

    @property
    def n_shift_types(self) -> int:
        return len(self.shift_ids)

    @property
    def n_weeks(self) -> int:
        return self.n_days // 7


def _split_nonempty(s: str, sep: str) -> List[str]:
    """Split on sep and drop empty pieces (handles trailing '|' or ',' with nothing after)."""
    return [p for p in s.split(sep) if p != ""]


def load_instance(path: str) -> Instance:
    """Parse one Nurse Rostering Benchmark instance file into an Instance.

    Handles: '#' comment lines and blank lines (skipped anywhere); multi-letter shift ids
    (e.g. 'd1', 'a2'); a forbidden-next list that can be empty; a MaxShifts field of the
    form 'E=14|D=14|L=0' (shift ids may repeat those already seen in SECTION_SHIFTS, in any
    order, and a count of 0 means "never assigned this shift").
    """
    name = path.split("/")[-1].split("\\")[-1].rsplit(".", 1)[0]

    n_days = 0
    shift_ids: List[str] = []
    shift_len: Dict[str, int] = {}
    forbidden_next: Dict[str, Set[str]] = {}

    nurse_ids: List[str] = []
    max_shifts: Dict[str, Dict[str, int]] = {}
    max_minutes: Dict[str, int] = {}
    min_minutes: Dict[str, int] = {}
    max_consec: Dict[str, int] = {}
    min_consec: Dict[str, int] = {}
    min_days_off: Dict[str, int] = {}
    max_weekends: Dict[str, int] = {}

    days_off: Dict[str, Set[int]] = {}
    on_requests: List[Tuple[str, int, str, int]] = []
    off_requests: List[Tuple[str, int, str, int]] = []
    cover: Dict[Tuple[int, str], Tuple[int, int, int]] = {}

    section = None
    with open(path, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("SECTION_"):
                section = line
                continue

            parts = line.split(",")

            if section == "SECTION_HORIZON":
                n_days = int(parts[0])

            elif section == "SECTION_SHIFTS":
                shift_id, length_min, forbidden = parts[0], parts[1], parts[2] if len(parts) > 2 else ""
                shift_ids.append(shift_id)
                shift_len[shift_id] = int(length_min)
                forbidden_next[shift_id] = set(_split_nonempty(forbidden, "|"))

            elif section == "SECTION_STAFF":
                nurse_id = parts[0]
                nurse_ids.append(nurse_id)
                ms: Dict[str, int] = {}
                for kv in _split_nonempty(parts[1], "|"):
                    shift, count = kv.split("=")
                    ms[shift] = int(count)
                max_shifts[nurse_id] = ms
                max_minutes[nurse_id] = int(parts[2])
                min_minutes[nurse_id] = int(parts[3])
                max_consec[nurse_id] = int(parts[4])
                min_consec[nurse_id] = int(parts[5])
                min_days_off[nurse_id] = int(parts[6])
                max_weekends[nurse_id] = int(parts[7])

            elif section == "SECTION_DAYS_OFF":
                nurse_id = parts[0]
                days = {int(d) for d in parts[1:] if d != ""}
                days_off.setdefault(nurse_id, set()).update(days)

            elif section == "SECTION_SHIFT_ON_REQUESTS":
                nurse_id, day, shift_id, weight = parts[0], int(parts[1]), parts[2], int(parts[3])
                on_requests.append((nurse_id, day, shift_id, weight))

            elif section == "SECTION_SHIFT_OFF_REQUESTS":
                nurse_id, day, shift_id, weight = parts[0], int(parts[1]), parts[2], int(parts[3])
                off_requests.append((nurse_id, day, shift_id, weight))

            elif section == "SECTION_COVER":
                day, shift_id, required, w_under, w_over = (
                    int(parts[0]), parts[1], int(parts[2]), int(parts[3]), int(parts[4])
                )
                cover[(day, shift_id)] = (required, w_under, w_over)

    # Every nurse has a days-off entry, even if empty, so callers never need .get() with a default.
    for nurse_id in nurse_ids:
        days_off.setdefault(nurse_id, set())

    return Instance(
        name=name,
        n_days=n_days,
        shift_ids=shift_ids,
        shift_len=shift_len,
        forbidden_next=forbidden_next,
        nurse_ids=nurse_ids,
        max_shifts=max_shifts,
        max_minutes=max_minutes,
        min_minutes=min_minutes,
        max_consec=max_consec,
        min_consec=min_consec,
        min_days_off=min_days_off,
        max_weekends=max_weekends,
        days_off=days_off,
        on_requests=on_requests,
        off_requests=off_requests,
        cover=cover,
    )


# ---------------------------------------------------------------------------
# Roster format (agreed convention, used by every notebook in this repo):
#   a numpy int array of shape (n_nurses, n_days), in nurse_ids / day order,
#   where 0 = day off and k = the k-th shift in Instance.shift_ids (1-based).
#
# Independent checker interface (implemented separately from this file, from
# the rule text alone, so the ILP and the GA are graded by the same referee
# that neither of them wrote):
#
#   def evaluate(roster: np.ndarray, inst: Instance) -> dict:
#       """Score one roster against one instance.
#
#       Returns
#       -------
#       dict with exactly these keys:
#         "penalty"  : float  -- the soft objective (cover under/over + unmet
#                                 shift-on/off requests), same units as the
#                                 ILP objective.
#         "hard"     : dict[str, float] -- one entry per hard rule (H1..H9),
#                                 the violation amount for that rule (0 if
#                                 satisfied).
#         "feasible" : bool   -- True iff every value in "hard" is 0.
#       """
#
# Hand-checks on Instance 1 that evaluate() must reproduce exactly:
#   all nurses off every day            -> penalty 7137
#   nurse A works the shift on days 2,3 -> penalty 6933
# ---------------------------------------------------------------------------
