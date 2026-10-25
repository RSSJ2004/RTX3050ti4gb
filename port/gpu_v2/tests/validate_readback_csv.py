#!/usr/bin/env python3
"""Validate that every readback diagnostic CSV row matches its header."""
from __future__ import annotations

import csv
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} READBACK.csv", file=sys.stderr)
        return 2

    path = sys.argv[1]
    with open(path, newline="", encoding="utf-8") as stream:
        rows = list(csv.reader(stream))

    if not rows:
        print("ERROR: CSV is empty", file=sys.stderr)
        return 1

    expected = len(rows[0])
    errors: list[tuple[int, int, list[str]]] = []
    for line_no, row in enumerate(rows[1:], start=2):
        if len(row) != expected:
            errors.append((line_no, len(row), row[:4]))

    if errors:
        for line_no, count, prefix in errors[:20]:
            print(
                f"ERROR line={line_no} fields={count} expected={expected} "
                f"prefix={prefix}",
                file=sys.stderr,
            )
        return 1

    print(f"OK header_fields={expected} data_rows={len(rows) - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
