from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins" / "theory-first" / "STATUS_MODEL.md"
TARGETS = (
    ROOT
    / "plugins"
    / "theory-first"
    / "skills"
    / "theory-first"
    / "references"
    / "status-model.md",
    ROOT
    / "plugins"
    / "theory-first"
    / "skills"
    / "theory-fix"
    / "references"
    / "status-model.md",
)


def synchronized() -> bool:
    expected = SOURCE.read_bytes()
    return all(target.is_file() and target.read_bytes() == expected for target in TARGETS)


def write_copies() -> None:
    content = SOURCE.read_bytes()
    for target in TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize skill-local status models for portable installs."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail instead of updating stale copies.",
    )
    args = parser.parse_args()

    if args.check:
        if synchronized():
            return 0
        print(
            "portable status-model copies are stale; run "
            "python scripts/sync_portable_resources.py",
            file=sys.stderr,
        )
        return 1

    write_copies()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
