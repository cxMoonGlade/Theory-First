from __future__ import annotations

import argparse
import base64
import configparser
import csv
import hashlib
import io
import subprocess
import tarfile
import zipfile
from email.parser import BytesParser
from email.policy import default
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.10 CI
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "plugins" / "theory-first" / "skills"
SOURCE = ROOT / "src" / "theory_first"
WHEEL_PREFIX = "theory_first/bundle/skills/"
WHEEL_CODE_PREFIX = "theory_first/"
SDIST_ROOT_FILES = (
    ".gitignore",
    "LICENSE",
    "README.md",
    "README.zh-CN.md",
    "pyproject.toml",
)


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def canonical_files() -> dict[str, str]:
    files: dict[str, str] = {}
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--",
            CANONICAL.relative_to(ROOT).as_posix(),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    tracked = [item for item in result.stdout.split(b"\0") if item]
    if not tracked:
        raise ValueError("git reported no canonical skill files")

    for relative_bytes in tracked:
        path = ROOT / relative_bytes.decode("utf-8")
        if path.is_symlink():
            raise ValueError(f"canonical skill contains a symbolic link: {path}")
        if not path.is_file():
            raise ValueError(f"tracked canonical skill file is missing: {path}")
        files[path.relative_to(CANONICAL).as_posix()] = digest(path.read_bytes())
    return files


def source_files() -> dict[str, str]:
    files = {
        path.relative_to(SOURCE).as_posix(): digest(path.read_bytes())
        for path in SOURCE.rglob("*.py")
        if path.is_file() and "__pycache__" not in path.parts
    }
    if not files:
        raise ValueError("no Python package source files found")
    return files


def wheel_files(
    path: Path,
) -> tuple[dict[str, str], dict[str, str], dict[str, bytes], bytes, bytes]:
    with zipfile.ZipFile(path) as archive:
        ordered_names = archive.namelist()
        names = set(ordered_names)
        if len(names) != len(ordered_names):
            raise ValueError("wheel contains duplicate archive members")
        members = {name: archive.read(name) for name in names}
        skills = {
            name.removeprefix(WHEEL_PREFIX): digest(members[name])
            for name in names
            if name.startswith(WHEEL_PREFIX) and not name.endswith("/")
        }
        code = {
            name.removeprefix(WHEEL_CODE_PREFIX): digest(members[name])
            for name in names
            if name.startswith(WHEEL_CODE_PREFIX)
            and name.endswith(".py")
            and not name.startswith(WHEEL_PREFIX)
        }
        metadata_names = [
            name for name in names if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_names) != 1:
            raise ValueError("wheel must contain exactly one METADATA file")
        metadata = members[metadata_names[0]]
        wheel_names = [name for name in names if name.endswith(".dist-info/WHEEL")]
        if len(wheel_names) != 1:
            raise ValueError("wheel must contain exactly one WHEEL file")
        wheel_metadata = members[wheel_names[0]]
    return skills, code, members, metadata, wheel_metadata


def sdist_files(
    path: Path, *, expected_root: str
) -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, bytes]]:
    skills: dict[str, str] = {}
    code: dict[str, str] = {}
    root_files: dict[str, str] = {}
    packaged_members: dict[str, bytes] = {}
    prefix = expected_root + "/"
    with tarfile.open(path, "r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        if len(names) != len(set(names)):
            raise ValueError("sdist contains duplicate archive members")
        for member in members:
            if not member.isfile():
                raise ValueError(
                    f"sdist contains a non-regular archive member: {member.name}"
                )
            if not member.name.startswith(prefix):
                raise ValueError(
                    f"sdist member is outside the expected root {expected_root}: "
                    f"{member.name}"
                )
            relative_member = member.name.removeprefix(prefix)
            if (
                not relative_member
                or relative_member.startswith("/")
                or ".." in Path(relative_member).parts
            ):
                raise ValueError(f"unsafe sdist member path: {member.name}")
            extracted = archive.extractfile(member)
            if extracted is None:
                raise ValueError(f"could not read sdist member: {member.name}")
            content = extracted.read()
            packaged_members[relative_member] = content
            if relative_member.startswith("plugins/theory-first/skills/"):
                relative = relative_member.removeprefix(
                    "plugins/theory-first/skills/"
                )
                skills[relative] = digest(content)
            elif relative_member.startswith("src/theory_first/") and member.name.endswith(
                ".py"
            ):
                relative = relative_member.removeprefix("src/theory_first/")
                code[relative] = digest(content)
            else:
                if relative_member in SDIST_ROOT_FILES:
                    root_files[relative_member] = digest(content)
    if set(root_files) != set(SDIST_ROOT_FILES):
        raise ValueError("sdist is missing a required root metadata file")
    return skills, code, root_files, packaged_members


def verify_metadata(content: bytes) -> None:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        project = tomllib.load(handle)["project"]
    metadata = BytesParser(policy=default).parsebytes(content)
    expected_headers = {
        "Name": project["name"],
        "Version": project["version"],
        "Summary": project["description"],
        "Requires-Python": project["requires-python"],
        "License-Expression": project["license"],
    }
    for header, expected in expected_headers.items():
        if metadata[header] != expected:
            raise ValueError(
                f"wheel {header} is stale: {metadata[header]!r} != {expected!r}"
            )
    if set(metadata.get_all("Classifier", [])) != set(project["classifiers"]):
        raise ValueError("wheel classifiers differ from pyproject.toml")
    runtime_requirements = [
        requirement
        for requirement in metadata.get_all("Requires-Dist", [])
        if "extra ==" not in requirement
    ]
    if runtime_requirements:
        raise ValueError(
            f"wheel unexpectedly has runtime dependencies: {runtime_requirements!r}"
        )
    description_type = metadata["Description-Content-Type"]
    if (
        description_type is None
        or description_type.split(";", 1)[0] != "text/markdown"
    ):
        raise ValueError("wheel long description is not Markdown")
    separator = b"\r\n\r\n" if b"\r\n\r\n" in content else b"\n\n"
    header, found, body = content.partition(separator)
    if not found or not header:
        raise ValueError("wheel METADATA has no header/body separator")
    try:
        long_description = body.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("wheel long description is not valid UTF-8") from error
    if long_description.rstrip("\n") != (
        ROOT / "README.md"
    ).read_text(encoding="utf-8").rstrip("\n"):
        raise ValueError("wheel long description differs from README.md")


def verify_wheel_record(content: bytes) -> None:
    wheel = BytesParser(policy=default).parsebytes(content)
    if wheel.get_all("Tag", []) != ["py3-none-any"]:
        raise ValueError("wheel must declare exactly the py3-none-any tag")


def _record_hash(content: bytes) -> str:
    encoded = base64.urlsafe_b64encode(hashlib.sha256(content).digest())
    return "sha256=" + encoded.rstrip(b"=").decode("ascii")


def verify_record(
    content: bytes, *, members: dict[str, bytes], record_name: str
) -> None:
    try:
        rows = list(csv.reader(io.StringIO(content.decode("utf-8"))))
    except (UnicodeDecodeError, csv.Error) as error:
        raise ValueError("wheel RECORD is not valid UTF-8 CSV") from error
    if any(len(row) != 3 for row in rows):
        raise ValueError("wheel RECORD rows must have exactly three fields")
    paths = [row[0] for row in rows]
    if len(paths) != len(set(paths)):
        raise ValueError("wheel RECORD contains duplicate paths")
    records = {row[0]: (row[1], row[2]) for row in rows}
    if set(records) != set(members):
        raise ValueError("wheel RECORD does not cover the exact wheel member set")
    for name, member_content in members.items():
        recorded_hash, recorded_size = records[name]
        if name == record_name:
            if recorded_hash or recorded_size:
                raise ValueError("wheel RECORD must leave its own hash and size empty")
            continue
        if recorded_hash != _record_hash(member_content):
            raise ValueError(f"wheel RECORD hash differs for {name}")
        if recorded_size != str(len(member_content)):
            raise ValueError(f"wheel RECORD size differs for {name}")


def verify_member_set(
    actual: set[str], expected: set[str], *, artifact: str
) -> None:
    if actual == expected:
        return
    extras = sorted(actual - expected)
    missing = sorted(expected - actual)
    raise ValueError(
        f"{artifact} member set is not closed; "
        f"extras={extras!r}, missing={missing!r}"
    )


def verify(wheel: Path, sdist: Path) -> None:
    expected = canonical_files()
    expected_code = source_files()
    with (ROOT / "pyproject.toml").open("rb") as handle:
        project = tomllib.load(handle)["project"]
    version = project["version"]
    dist_info = f"theory_first-{version}.dist-info"
    sdist_root = f"theory_first-{version}"
    (
        packaged_wheel,
        wheel_code,
        wheel_members,
        metadata,
        wheel_record,
    ) = wheel_files(wheel)
    (
        packaged_sdist,
        sdist_code,
        sdist_root_files,
        sdist_members,
    ) = sdist_files(sdist, expected_root=sdist_root)

    expected_wheel_members = {
        *(f"{WHEEL_PREFIX}{relative}" for relative in expected),
        *(f"{WHEEL_CODE_PREFIX}{relative}" for relative in expected_code),
        f"{dist_info}/METADATA",
        f"{dist_info}/WHEEL",
        f"{dist_info}/entry_points.txt",
        f"{dist_info}/licenses/LICENSE",
        f"{dist_info}/RECORD",
    }
    verify_member_set(
        set(wheel_members), expected_wheel_members, artifact="wheel"
    )

    expected_sdist_members = {
        *(f"plugins/theory-first/skills/{relative}" for relative in expected),
        *(f"src/theory_first/{relative}" for relative in expected_code),
        *SDIST_ROOT_FILES,
        "PKG-INFO",
    }
    verify_member_set(
        set(sdist_members), expected_sdist_members, artifact="sdist"
    )

    if packaged_wheel != expected:
        raise ValueError("wheel skill payload differs from canonical skills")
    if packaged_sdist != expected:
        raise ValueError("sdist skill payload differs from canonical skills")
    if wheel_code != expected_code:
        raise ValueError("wheel Python code differs from current package source")
    if sdist_code != expected_code:
        raise ValueError("sdist Python code differs from current package source")
    for filename in SDIST_ROOT_FILES:
        if sdist_root_files[filename] != digest((ROOT / filename).read_bytes()):
            raise ValueError(f"sdist {filename} differs from the current source")
    license_name = f"{dist_info}/licenses/LICENSE"
    if digest(wheel_members[license_name]) != digest((ROOT / "LICENSE").read_bytes()):
        raise ValueError("wheel license differs from LICENSE")
    verify_metadata(metadata)
    verify_metadata(sdist_members["PKG-INFO"])
    verify_wheel_record(wheel_record)

    record_name = f"{dist_info}/RECORD"
    verify_record(
        wheel_members[record_name], members=wheel_members, record_name=record_name
    )

    entry_points = [
        name
        for name in wheel_members
        if name.endswith(".dist-info/entry_points.txt")
    ]
    if len(entry_points) != 1:
        raise ValueError("wheel must contain exactly one entry_points.txt")
    content = wheel_members[entry_points[0]].decode("utf-8")
    entry_point_config = configparser.ConfigParser()
    entry_point_config.read_file(io.StringIO(content))
    if dict(entry_point_config["console_scripts"]) != {
        "theory-first": "theory_first.cli:main"
    }:
        raise ValueError("wheel console entry points differ from the contract")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify that Python artifacts contain the canonical skills."
    )
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--sdist", type=Path, required=True)
    args = parser.parse_args()
    verify(args.wheel, args.sdist)
    print("Python distribution payload matches the canonical seven-skill suite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
