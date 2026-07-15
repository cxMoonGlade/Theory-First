from __future__ import annotations

import stat
from pathlib import Path


EXPECTED_SKILLS = (
    "close-literature",
    "deep-read-paper",
    "map-research-landscape",
    "preregister-claim",
    "stress-test-claim",
    "theory-first",
    "theory-fix",
)


class BundleError(RuntimeError):
    """Raised when the packaged skill bundle is missing or malformed."""


def _is_linklike(path: Path) -> bool:
    """Return whether *path* is a symlink or Windows reparse-point directory."""

    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    if is_junction is not None and is_junction():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except (FileNotFoundError, OSError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _candidate_roots() -> tuple[Path, ...]:
    installed = Path(__file__).resolve().parent / "bundle" / "skills"
    checkout = (
        Path(__file__).resolve().parents[2]
        / "plugins"
        / "theory-first"
        / "skills"
    )
    return installed, checkout


def validate_bundle(root: Path) -> Path:
    if _is_linklike(root) or not root.is_dir():
        raise BundleError(f"skill bundle is not a directory: {root}")

    children = tuple(root.iterdir())
    actual = {path.name for path in children}
    expected = set(EXPECTED_SKILLS)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise BundleError(
            f"skill bundle mismatch; missing={missing!r}, extra={extra!r}"
        )

    for skill_name in EXPECTED_SKILLS:
        skill_root = root / skill_name
        if _is_linklike(skill_root) or not skill_root.is_dir():
            raise BundleError(f"skill root is not a regular directory: {skill_name}")
        if not (skill_root / "SKILL.md").is_file():
            raise BundleError(f"missing SKILL.md for {skill_name}")
        for path in skill_root.rglob("*"):
            if _is_linklike(path):
                raise BundleError(
                    f"symbolic link or reparse point found in packaged skill: "
                    f"{skill_name}"
                )
            if not (path.is_dir() or path.is_file()):
                raise BundleError(
                    f"non-regular resource found in packaged skill: {path}"
                )

    return root


def bundle_root() -> Path:
    failures: list[str] = []
    for candidate in _candidate_roots():
        try:
            return validate_bundle(candidate)
        except BundleError as error:
            failures.append(str(error))
    raise BundleError("no valid bundled skills found: " + "; ".join(failures))
