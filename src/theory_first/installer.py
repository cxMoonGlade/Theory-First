from __future__ import annotations

import hashlib
import os
import shutil
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .bundle import EXPECTED_SKILLS, bundle_root


AGENTS = ("codex", "claude-code", "opencode")


class InstallError(RuntimeError):
    """Raised when a safe complete-suite installation cannot proceed."""


@dataclass(frozen=True)
class InstallResult:
    target: Path
    skills: tuple[str, ...]
    dry_run: bool


@dataclass
class _InstallAttempt:
    skill_name: str
    device: int
    inode: int
    manifest: dict[str, str]


@dataclass
class _PreparedInstall:
    target: Path
    staging: Path
    backup: Path
    target_existed: bool
    install_attempts: list[_InstallAttempt]
    backup_attempts: list[str]


@dataclass
class _InstallLock:
    path: Path
    descriptor: int
    device: int
    inode: int


def _expanded(path: str | os.PathLike[str]) -> Path:
    return Path(path).expanduser().resolve()


def target_for(
    agent: str,
    *,
    scope: str = "user",
    project: str | os.PathLike[str] | None = None,
) -> Path:
    if agent not in AGENTS:
        raise InstallError(f"unsupported agent {agent!r}; choose from {AGENTS!r}")
    if scope not in {"user", "project"}:
        raise InstallError("scope must be 'user' or 'project'")

    if scope == "project":
        if project is None:
            raise InstallError("--project is required with --scope project")
        root = _expanded(project)
        relative = {
            "codex": Path(".agents/skills"),
            "claude-code": Path(".claude/skills"),
            "opencode": Path(".opencode/skills"),
        }[agent]
        return root / relative

    if project is not None:
        raise InstallError("--project is only valid with --scope project")

    home = Path.home()
    if agent == "codex":
        return _expanded(home / ".agents" / "skills")
    if agent == "claude-code":
        return _expanded(
            Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude")) / "skills"
        )
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
    return _expanded(config_home / "opencode" / "skills")


def _exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _is_linklike(path: Path) -> bool:
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


def _assert_safe_target(target: Path, source: Path) -> None:
    resolved_target = target.resolve()
    resolved_source = source.resolve()
    if resolved_target == resolved_source:
        raise InstallError("installation target cannot be the bundled source")
    if resolved_target in resolved_source.parents:
        raise InstallError("installation target cannot contain the bundled source")
    if resolved_source in resolved_target.parents:
        raise InstallError("installation target cannot be inside the bundled source")


def conflicts(target: Path) -> tuple[str, ...]:
    return tuple(
        skill_name
        for skill_name in EXPECTED_SKILLS
        if _exists(target / skill_name)
    )


def _remove_path(path: Path) -> None:
    if _is_linklike(path) or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _rollback(prepared: _PreparedInstall) -> list[str]:
    errors: list[str] = []
    for attempt in reversed(prepared.install_attempts):
        skill_name = attempt.skill_name
        staged_path = prepared.staging / skill_name
        final_path = prepared.target / skill_name
        try:
            # The attempt is recorded before os.replace. A missing staged path
            # proves that the rename completed even if Python was interrupted
            # before the call returned to our bytecode.
            if not _exists(staged_path) and _exists(final_path):
                if _is_linklike(final_path):
                    errors.append(
                        f"installed path changed; preserved link-like path: {final_path}"
                    )
                    continue
                identity = final_path.lstat()
                if (identity.st_dev, identity.st_ino) != (
                    attempt.device,
                    attempt.inode,
                ):
                    errors.append(
                        f"installed path identity changed; preserved {final_path}"
                    )
                    continue
                if _tree_manifest(final_path) != attempt.manifest:
                    errors.append(
                        f"installed path content changed; preserved {final_path}"
                    )
                    continue
                _remove_path(final_path)
        except BaseException as error:
            errors.append(f"remove {final_path}: {error}")

    for skill_name in reversed(prepared.backup_attempts):
        backup_path = prepared.backup / skill_name
        final_path = prepared.target / skill_name
        try:
            # As above, an attempted backup move only changed state when its
            # destination exists. Never disturb a final path otherwise.
            if not _exists(backup_path):
                continue
            if _exists(final_path):
                errors.append(f"restore blocked by existing path: {final_path}")
            else:
                os.replace(backup_path, final_path)
        except BaseException as error:
            errors.append(f"restore {final_path}: {error}")

    shutil.rmtree(prepared.staging, ignore_errors=True)
    if not errors:
        shutil.rmtree(prepared.backup, ignore_errors=True)
        if not prepared.target_existed:
            try:
                prepared.target.rmdir()
            except OSError:
                pass
    return errors


def _tree_manifest(root: Path) -> dict[str, str]:
    if _is_linklike(root) or not root.is_dir():
        raise InstallError(f"skill root is not a regular directory: {root}")
    manifest: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if _is_linklike(path):
            raise InstallError(f"symbolic link or junction found in skill tree: {path}")
        relative = path.relative_to(root).as_posix()
        if path.is_dir():
            manifest[f"{relative}/"] = "directory"
            continue
        if path.is_file():
            manifest[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
            continue
        raise InstallError(f"non-regular resource found in skill tree: {path}")
    return manifest


def _assert_independent_targets(targets: tuple[Path, ...]) -> None:
    for index, first in enumerate(targets):
        for second in targets[index + 1 :]:
            if first in second.parents or second in first.parents:
                raise InstallError(
                    f"installation targets cannot contain one another: "
                    f"{first}, {second}"
                )


def _acquire_locks(targets: tuple[Path, ...]) -> list[_InstallLock]:
    locks: list[_InstallLock] = []
    locked_parents: set[tuple[int, int]] = set()
    try:
        for target in sorted(targets, key=str):
            target.parent.mkdir(parents=True, exist_ok=True)
            parent_identity = target.parent.stat()
            parent_key = (parent_identity.st_dev, parent_identity.st_ino)
            if parent_key in locked_parents:
                continue
            # One fixed lock per physical parent directory prevents two
            # cooperating installers from bypassing one another with different
            # target spellings on a case-insensitive filesystem. Targets that
            # share a parent are intentionally serialized.
            lock_path = target.parent / ".theory-first-install.lock"
            try:
                descriptor = os.open(
                    lock_path,
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600,
                )
            except FileExistsError as error:
                raise InstallError(
                    f"another install may own {lock_path}; if no installer is "
                    "running, inspect the directory before removing the stale lock"
                ) from error
            identity_stat = os.fstat(descriptor)
            locks.append(
                _InstallLock(
                    lock_path,
                    descriptor,
                    identity_stat.st_dev,
                    identity_stat.st_ino,
                )
            )
            locked_parents.add(parent_key)
            os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
    except BaseException:
        _release_locks(locks)
        raise
    return locks


def _release_locks(locks: Iterable[_InstallLock]) -> list[str]:
    errors: list[str] = []
    for lock in reversed(tuple(locks)):
        try:
            os.close(lock.descriptor)
        except OSError as error:
            errors.append(f"close {lock.path}: {error}")
        try:
            current = lock.path.lstat()
        except FileNotFoundError:
            continue
        except OSError as error:
            errors.append(f"inspect {lock.path}: {error}")
            continue
        if (current.st_dev, current.st_ino) != (lock.device, lock.inode):
            errors.append(f"lock identity changed; preserved {lock.path}")
            continue
        try:
            lock.path.unlink()
        except OSError as error:
            errors.append(f"remove {lock.path}: {error}")
    return errors


def _raise_if_blocked(targets: tuple[Path, ...], *, force: bool) -> None:
    blocked: dict[Path, tuple[str, ...]] = {}
    if not force:
        for destination in targets:
            existing = conflicts(destination)
            if existing:
                blocked[destination] = existing
    if blocked:
        details = "; ".join(
            f"{target}: {', '.join(names)}" for target, names in blocked.items()
        )
        raise InstallError(
            f"existing skill paths block the complete install: {details}; "
            "rerun with --force to replace them"
        )


def _perform_install(
    source: Path,
    destinations: tuple[Path, ...],
    results: tuple[InstallResult, ...],
    *,
    force: bool,
) -> tuple[InstallResult, ...]:
    source_manifests = {
        skill_name: _tree_manifest(source / skill_name)
        for skill_name in EXPECTED_SKILLS
    }
    prepared_installs: list[_PreparedInstall] = []
    try:
        for destination in destinations:
            target_existed = _exists(destination)
            if target_existed and not destination.is_dir():
                raise InstallError(
                    f"installation target is not a directory: {destination}"
                )
            destination.mkdir(parents=True, exist_ok=True)
            staging = Path(
                tempfile.mkdtemp(
                    prefix=".theory-first-stage-", dir=destination.parent
                )
            )
            try:
                backup = Path(
                    tempfile.mkdtemp(
                        prefix=".theory-first-backup-", dir=destination.parent
                    )
                )
            except BaseException:
                shutil.rmtree(staging, ignore_errors=True)
                if not target_existed:
                    try:
                        destination.rmdir()
                    except OSError:
                        pass
                raise
            prepared = _PreparedInstall(
                target=destination,
                staging=staging,
                backup=backup,
                target_existed=target_existed,
                install_attempts=[],
                backup_attempts=[],
            )
            prepared_installs.append(prepared)
            for skill_name in EXPECTED_SKILLS:
                staged_skill = staging / skill_name
                shutil.copytree(source / skill_name, staged_skill)
                if _tree_manifest(staged_skill) != source_manifests[skill_name]:
                    raise InstallError(f"staged skill differs from source: {skill_name}")

        if not force:
            raced: dict[Path, tuple[str, ...]] = {}
            for prepared in prepared_installs:
                existing = conflicts(prepared.target)
                if existing:
                    raced[prepared.target] = existing
            if raced:
                details = "; ".join(
                    f"{target}: {', '.join(names)}"
                    for target, names in raced.items()
                )
                raise InstallError(
                    "skill directories appeared while preparing the install: "
                    + details
                )

        for prepared in prepared_installs:
            for skill_name in EXPECTED_SKILLS:
                final_path = prepared.target / skill_name
                if _exists(final_path):
                    if not force:
                        raise InstallError(
                            f"skill path appeared during installation: {final_path}"
                        )
                    # Record intent before each destructive rename. Rollback
                    # inspects the source/destination state, so interrupts on
                    # either side of the syscall remain recoverable.
                    prepared.backup_attempts.append(skill_name)
                    os.replace(final_path, prepared.backup / skill_name)
                staged_path = prepared.staging / skill_name
                staged_identity = staged_path.lstat()
                prepared.install_attempts.append(
                    _InstallAttempt(
                        skill_name=skill_name,
                        device=staged_identity.st_dev,
                        inode=staged_identity.st_ino,
                        manifest=source_manifests[skill_name],
                    )
                )
                # `os.replace` may overwrite a path created after our final
                # conflict check on Windows. `os.rename` refuses that existing
                # destination there; on POSIX, a staged directory cannot replace
                # a concurrently created regular file. This preserves the
                # external writer used by the commit-race regression test.
                os.rename(staged_path, final_path)
    except BaseException as error:
        rollback_errors: list[str] = []
        for prepared in reversed(prepared_installs):
            rollback_errors.extend(_rollback(prepared))
        if rollback_errors:
            recovery_paths = ", ".join(
                str(prepared.backup) for prepared in prepared_installs
            )
            details = "; ".join(rollback_errors)
            raise InstallError(
                f"installation failed and rollback was incomplete: {details}; "
                f"preserved recovery data under {recovery_paths}"
            ) from error
        raise

    # Every target now contains the complete verified suite. This is the commit
    # boundary: an error before it enters the rollback path above; an interrupt
    # during best-effort cleanup must not attempt to restore a backup that may
    # already be partially deleted.
    try:
        for prepared in prepared_installs:
            shutil.rmtree(prepared.staging)
            shutil.rmtree(prepared.backup)
    except BaseException as error:
        leftovers = [
            path
            for prepared in prepared_installs
            for path in (prepared.staging, prepared.backup)
            if _exists(path)
        ]
        details = (
            "; inspect leftover transaction data under "
            + ", ".join(str(path) for path in leftovers)
            if leftovers
            else "; no transaction directory remains"
        )
        raise InstallError(
            "installation was committed, but transaction cleanup was "
            f"interrupted or failed; the installed skills are active{details}"
        ) from error
    return results


def install_suites(
    targets: Iterable[str | os.PathLike[str]],
    *,
    force: bool = False,
    dry_run: bool = False,
) -> tuple[InstallResult, ...]:
    source = bundle_root()
    destinations = unique_targets(_expanded(target) for target in targets)
    if not destinations:
        raise InstallError("at least one installation target is required")
    _assert_independent_targets(destinations)

    for destination in destinations:
        _assert_safe_target(destination, source)

    results = tuple(
        InstallResult(destination, EXPECTED_SKILLS, dry_run)
        for destination in destinations
    )
    if dry_run:
        _raise_if_blocked(destinations, force=force)
        return results

    locks = _acquire_locks(destinations)
    try:
        _raise_if_blocked(destinations, force=force)
        completed = _perform_install(source, destinations, results, force=force)
    except BaseException as error:
        release_errors = _release_locks(locks)
        if release_errors and hasattr(error, "add_note"):
            error.add_note("lock cleanup also failed: " + "; ".join(release_errors))
        raise

    release_errors = _release_locks(locks)
    if release_errors:
        raise InstallError(
            "installation was committed, but lock cleanup was incomplete; "
            "the installed skills are active: "
            + "; ".join(release_errors)
        )
    return completed


def install_suite(
    target: str | os.PathLike[str],
    *,
    force: bool = False,
    dry_run: bool = False,
) -> InstallResult:
    return install_suites((target,), force=force, dry_run=dry_run)[0]


def unique_targets(paths: Iterable[Path]) -> tuple[Path, ...]:
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return tuple(unique)
