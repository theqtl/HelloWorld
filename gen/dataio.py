"""CSV loading helpers. Single source of truth = data/*.csv."""
import csv
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_rows(name):
    """Load data/<name>.csv as a list of dict rows."""
    path = os.path.join(DATA_DIR, name + ".csv")
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_params():
    """Return {param_id: row} for parameters.csv."""
    return {r["param_id"]: r for r in load_rows("parameters")}


def param_value(params, pid):
    """Float value of a parameter, or None if blank/unparseable.

    Never invents a value: a blank stays None so callers can flag a gap.
    """
    row = params.get(pid)
    if not row:
        return None
    raw = (row.get("value") or "").strip()
    if raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None
