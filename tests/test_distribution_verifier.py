from __future__ import annotations

import base64
import csv
import hashlib
import io
import tarfile
from pathlib import Path

import pytest

from scripts.verify_python_distribution import (
    ROOT,
    sdist_files,
    verify_member_set,
    verify_metadata,
    verify_record,
)


def _hash(content: bytes) -> str:
    value = base64.urlsafe_b64encode(hashlib.sha256(content).digest())
    return "sha256=" + value.rstrip(b"=").decode("ascii")


def test_metadata_long_description_preserves_non_ascii_readme() -> None:
    readme = (ROOT / "README.md").read_bytes()
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering",
    ]
    headers = [
        "Metadata-Version: 2.4",
        "Name: theory-first",
        "Version: 0.3.0",
        "Summary: Cross-platform evidence gates for rigorous computational science",
        "Requires-Python: >=3.10",
        "License-Expression: MIT",
        *(f"Classifier: {classifier}" for classifier in classifiers),
        "Description-Content-Type: text/markdown",
    ]
    metadata = "\n".join(headers).encode("utf-8") + b"\n\n" + readme

    verify_metadata(metadata)


def test_closed_member_set_rejects_an_untracked_extra() -> None:
    with pytest.raises(ValueError, match="not closed"):
        verify_member_set(
            {"expected.py", "untracked-secret.txt"},
            {"expected.py"},
            artifact="wheel",
        )


def test_wheel_record_covers_and_hashes_every_member() -> None:
    payload = b"payload"
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("theory_first/example.py", _hash(payload), len(payload)))
    writer.writerow(("theory_first-0.3.0.dist-info/RECORD", "", ""))
    record = output.getvalue().encode("utf-8")
    members = {
        "theory_first/example.py": payload,
        "theory_first-0.3.0.dist-info/RECORD": record,
    }

    verify_record(
        record,
        members=members,
        record_name="theory_first-0.3.0.dist-info/RECORD",
    )

    members["theory_first/untracked-secret.txt"] = b"secret"
    with pytest.raises(ValueError, match="exact wheel member set"):
        verify_record(
            record,
            members=members,
            record_name="theory_first-0.3.0.dist-info/RECORD",
        )


def test_sdist_rejects_symbolic_link_members(tmp_path: Path) -> None:
    archive_path = tmp_path / "unsafe.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        member = tarfile.TarInfo("theory_first-0.3.0/linked")
        member.type = tarfile.SYMTYPE
        member.linkname = "../../outside"
        archive.addfile(member)

    with pytest.raises(ValueError, match="non-regular"):
        sdist_files(archive_path, expected_root="theory_first-0.3.0")
