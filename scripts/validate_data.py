"""Lightweight validation for the committed cleaned flight snapshot."""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path


REQUIRED_COLUMNS = {
    "icao24",
    "callsign",
    "origin_country",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "geo_altitude",
    "price",
}


def optional_number(value: str, field: str, row_number: int) -> float | None:
    """Parse an optional finite numeric value and report its source on failure."""
    if value.strip() == "":
        return None

    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"row {row_number}: {field} is not numeric") from exc

    if not math.isfinite(number):
        raise ValueError(f"row {row_number}: {field} is not finite")
    return number


def validate_csv(path: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    identifiers: Counter[str] = Counter()

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - headers)
        if missing:
            return 0, [f"missing required columns: {', '.join(missing)}"]

        row_count = 0
        for row_number, row in enumerate(reader, start=2):
            row_count += 1
            identifier = row["icao24"].strip().lower()
            if identifier:
                identifiers[identifier] += 1

            try:
                latitude = optional_number(row["latitude"], "latitude", row_number)
                longitude = optional_number(row["longitude"], "longitude", row_number)
                velocity = optional_number(row["velocity"], "velocity", row_number)
                optional_number(row["baro_altitude"], "baro_altitude", row_number)
                optional_number(row["geo_altitude"], "geo_altitude", row_number)
            except ValueError as exc:
                errors.append(str(exc))
                continue

            if latitude is None or not -90 <= latitude <= 90:
                errors.append(f"row {row_number}: latitude must be between -90 and 90")
            if longitude is None or not -180 <= longitude <= 180:
                errors.append(f"row {row_number}: longitude must be between -180 and 180")
            if velocity is not None and velocity < 0:
                errors.append(f"row {row_number}: velocity must be non-negative")

    duplicates = sorted(identifier for identifier, count in identifiers.items() if count > 1)
    if duplicates:
        preview = ", ".join(duplicates[:10])
        suffix = " ..." if len(duplicates) > 10 else ""
        errors.append(
            f"duplicate icao24 observations ({len(duplicates)} identifiers): "
            f"{preview}{suffix}"
        )

    return row_count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        default=Path("data/processed/flights_clean.csv"),
        help="cleaned CSV to validate (default: data/processed/flights_clean.csv)",
    )
    args = parser.parse_args()

    if not args.csv_path.is_file():
        print(f"FAIL: file not found: {args.csv_path}")
        return 1

    row_count, errors = validate_csv(args.csv_path)
    if errors:
        print(f"FAIL: {len(errors)} validation issue(s) in {row_count} rows")
        for error in errors[:20]:
            print(f"- {error}")
        if len(errors) > 20:
            print(f"- ... {len(errors) - 20} more")
        return 1

    print(f"PASS: {row_count} rows validated; required columns present")
    print("PASS: coordinates, velocity, and altitude fields satisfy basic checks")
    print("PASS: no duplicate icao24 observations found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
