from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

import theory_first.installer as installer_module
from theory_first.bundle import EXPECTED_SKILLS, bundle_root, validate_bundle
from theory_first.cli import main
from theory_first.installer import (
    InstallError,
    install_suite,
    install_suites,
    target_for,
)


def test_source_bundle_is_complete_and_valid() -> None:
    root = validate_bundle(bundle_root())
    assert {path.name for path in root.iterdir() if path.is_dir()} == set(
        EXPECTED_SKILLS
    )
    assert all((root / name / "SKILL.md").is_file() for name in EXPECTED_SKILLS)


def test_dry_run_does_not_create_the_target(tmp_path: Path) -> None:
    target = tmp_path / "skills"
    result = install_suite(target, dry_run=True)
    assert result.dry_run is True
    assert result.target == target.resolve()
    assert result.skills == EXPECTED_SKILLS
    assert not target.exists()


def test_install_copies_the_complete_suite(tmp_path: Path) -> None:
    target = tmp_path / "skills"
    result = install_suite(target)
    assert result.dry_run is False
    assert {path.name for path in target.iterdir() if path.is_dir()} == set(
        EXPECTED_SKILLS
    )
    source = bundle_root()
    for skill_name in EXPECTED_SKILLS:
        assert (target / skill_name / "SKILL.md").read_bytes() == (
            source / skill_name / "SKILL.md"
        ).read_bytes()


def test_existing_skill_blocks_the_whole_install(tmp_path: Path) -> None:
    target = tmp_path / "skills"
    existing = target / "theory-first"
    existing.mkdir(parents=True)
    marker = existing / "user-content.txt"
    marker.write_text("keep", encoding="utf-8")

    with pytest.raises(InstallError, match="--force"):
        install_suite(target)

    assert marker.read_text(encoding="utf-8") == "keep"
    assert {path.name for path in target.iterdir()} == {"theory-first"}


@pytest.mark.parametrize("path_kind", ("file", "dangling-symlink"))
def test_existing_non_directory_skill_path_blocks_the_whole_install(
    tmp_path: Path, path_kind: str
) -> None:
    target = tmp_path / "skills"
    target.mkdir()
    existing = target / "theory-first"
    if path_kind == "file":
        existing.write_text("keep", encoding="utf-8")
    else:
        try:
            existing.symlink_to(
                tmp_path / "missing-skill", target_is_directory=True
            )
        except OSError as error:
            pytest.skip(f"directory symlinks are unavailable: {error}")

    with pytest.raises(InstallError, match="--force"):
        install_suite(target)

    assert existing.is_file() if path_kind == "file" else existing.is_symlink()


def test_force_replaces_only_the_seven_owned_skill_names(tmp_path: Path) -> None:
    target = tmp_path / "skills"
    stale = target / "theory-first"
    stale.mkdir(parents=True)
    (stale / "SKILL.md").write_text("stale", encoding="utf-8")
    unrelated = target / "user-skill"
    unrelated.mkdir()
    (unrelated / "SKILL.md").write_text("user", encoding="utf-8")

    install_suite(target, force=True)

    assert (target / "theory-first" / "SKILL.md").read_bytes() == (
        bundle_root() / "theory-first" / "SKILL.md"
    ).read_bytes()
    assert (unrelated / "SKILL.md").read_text(encoding="utf-8") == "user"


def test_force_replaces_a_symlink_without_touching_its_target(
    tmp_path: Path,
) -> None:
    target = tmp_path / "skills"
    target.mkdir()
    external = tmp_path / "external-user-skill"
    external.mkdir()
    marker = external / "user-content.txt"
    marker.write_text("keep", encoding="utf-8")
    link = target / "theory-first"
    try:
        link.symlink_to(external, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"directory symlinks are unavailable: {error}")

    install_suite(target, force=True)

    assert not link.is_symlink()
    assert (link / "SKILL.md").is_file()
    assert marker.read_text(encoding="utf-8") == "keep"


def test_native_user_and_project_targets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude-home"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config-home"))

    # Codex's public Agent Skills path is HOME/.agents/skills. CODEX_HOME is
    # deliberately irrelevant to user skill discovery.
    assert target_for("codex") == (tmp_path / "home/.agents/skills").resolve()
    assert target_for("claude-code") == (
        tmp_path / "claude-home/skills"
    ).resolve()
    assert target_for("opencode") == (
        tmp_path / "config-home/opencode/skills"
    ).resolve()

    project = tmp_path / "project"
    assert target_for("codex", scope="project", project=project) == (
        project / ".agents/skills"
    ).resolve()
    assert target_for("claude-code", scope="project", project=project) == (
        project / ".claude/skills"
    ).resolve()
    assert target_for("opencode", scope="project", project=project) == (
        project / ".opencode/skills"
    ).resolve()


def test_multi_host_cli_reuses_an_opencode_compatible_skill_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))

    assert main(
        [
            "install",
            "--agent",
            "codex",
            "--agent",
            "claude-code",
            "--agent",
            "opencode",
            "--dry-run",
        ]
    ) == 0

    output = capsys.readouterr().out
    assert str((tmp_path / "home/.agents/skills").resolve()) in output
    assert str((tmp_path / "claude/skills").resolve()) in output
    assert str((tmp_path / "config/opencode/skills").resolve()) not in output
    assert not (tmp_path / "home").exists()


def test_custom_claude_home_does_not_suppress_the_native_opencode_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "custom-claude"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))

    assert main(
        [
            "install",
            "--agent",
            "claude-code",
            "--agent",
            "opencode",
            "--dry-run",
        ]
    ) == 0

    output = capsys.readouterr().out
    assert str((tmp_path / "custom-claude/skills").resolve()) in output
    assert str((tmp_path / "config/opencode/skills").resolve()) in output


def test_cli_lists_and_installs_to_an_explicit_target(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["list"]) == 0
    assert capsys.readouterr().out.splitlines() == list(EXPECTED_SKILLS)

    target = tmp_path / "custom-skills"
    assert main(["install", "--target", str(target)]) == 0
    output = capsys.readouterr().out
    assert f"installed 7 skills -> {target.resolve()}" in output
    assert all((target / name / "SKILL.md").is_file() for name in EXPECTED_SKILLS)


def test_project_scope_requires_a_project() -> None:
    assert main(["install", "--agent", "codex", "--scope", "project"]) == 2


def test_nested_installation_targets_are_rejected(tmp_path: Path) -> None:
    outer = tmp_path / "skills"
    inner = outer / "nested-skills"
    with pytest.raises(InstallError, match="contain one another"):
        install_suites((outer, inner), dry_run=True)


def test_source_overlap_is_rejected_without_writes() -> None:
    source_parent = bundle_root().parent
    with pytest.raises(InstallError, match="bundled source"):
        install_suite(source_parent, dry_run=True)


def _seed_stale_skill(target: Path, marker_text: str) -> Path:
    stale = target / "theory-first"
    stale.mkdir(parents=True)
    marker = stale / "user-content.txt"
    marker.write_text(marker_text, encoding="utf-8")
    return marker


def test_second_target_failure_rolls_back_every_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first = tmp_path / "first-skills"
    second = tmp_path / "second-skills"
    first_marker = _seed_stale_skill(first, "first")
    second_marker = _seed_stale_skill(second, "second")
    real_rename = os.rename

    def fail_second_target_install(
        source: str | os.PathLike[str], destination: str | os.PathLike[str]
    ) -> None:
        source_path = Path(source)
        destination_path = Path(destination)
        if (
            destination_path == second / "theory-first"
            and source_path.parent.name.startswith(".theory-first-stage-")
        ):
            raise OSError("injected second-target failure")
        real_rename(source, destination)

    monkeypatch.setattr(installer_module.os, "rename", fail_second_target_install)

    with pytest.raises(OSError, match="injected second-target failure"):
        install_suites((first, second), force=True)

    assert first_marker.read_text(encoding="utf-8") == "first"
    assert second_marker.read_text(encoding="utf-8") == "second"
    assert {path.name for path in first.iterdir()} == {"theory-first"}
    assert {path.name for path in second.iterdir()} == {"theory-first"}
    assert not tuple(tmp_path.glob(".theory-first-*"))


def test_targets_with_the_same_parent_share_one_cooperative_lock(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first-skills"
    second = tmp_path / "second-skills"

    install_suites((first, second))

    for target in (first, second):
        assert {path.name for path in target.iterdir()} == set(EXPECTED_SKILLS)
    assert not tuple(tmp_path.glob(".theory-first-*.lock"))


def test_keyboard_interrupt_after_backup_restores_the_old_skill(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "skills"
    marker = _seed_stale_skill(target, "old")
    real_rename = os.rename

    def interrupt_install(
        source: str | os.PathLike[str], destination: str | os.PathLike[str]
    ) -> None:
        source_path = Path(source)
        destination_path = Path(destination)
        if (
            destination_path == target / "theory-first"
            and source_path.parent.name.startswith(".theory-first-stage-")
        ):
            raise KeyboardInterrupt
        real_rename(source, destination)

    monkeypatch.setattr(installer_module.os, "rename", interrupt_install)

    with pytest.raises(KeyboardInterrupt):
        install_suite(target, force=True)

    assert marker.read_text(encoding="utf-8") == "old"
    assert {path.name for path in target.iterdir()} == {"theory-first"}
    assert not tuple(tmp_path.glob(".theory-first-*"))


@pytest.mark.parametrize("interrupt_phase", ("backup", "install"))
def test_interrupt_immediately_after_a_successful_rename_restores_the_old_skill(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    interrupt_phase: str,
) -> None:
    target = tmp_path / "skills"
    marker = _seed_stale_skill(target, "precious")
    real_replace = os.replace
    real_rename = os.rename

    def interrupt_after_success(
        source: str | os.PathLike[str], destination: str | os.PathLike[str]
    ) -> None:
        source_path = Path(source)
        destination_path = Path(destination)
        is_backup = (
            source_path == target / "theory-first"
            and destination_path.parent.name.startswith(".theory-first-backup-")
        )
        is_install = (
            destination_path == target / "theory-first"
            and source_path.parent.name.startswith(".theory-first-stage-")
        )
        operation = real_replace if is_backup else real_rename
        if (interrupt_phase == "backup" and is_backup) or (
            interrupt_phase == "install" and is_install
        ):
            operation(source, destination)
            raise KeyboardInterrupt
        operation(source, destination)

    monkeypatch.setattr(installer_module.os, "replace", interrupt_after_success)
    monkeypatch.setattr(installer_module.os, "rename", interrupt_after_success)

    with pytest.raises(KeyboardInterrupt):
        install_suite(target, force=True)

    assert marker.read_text(encoding="utf-8") == "precious"
    assert {path.name for path in target.iterdir()} == {"theory-first"}
    assert not tuple(tmp_path.glob(".theory-first-*"))


def test_interrupt_during_post_commit_cleanup_reports_active_install_and_backup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "skills"
    _seed_stale_skill(target, "precious")
    real_rmtree = shutil.rmtree

    def interrupt_backup_cleanup(
        path: str | os.PathLike[str], *args: object, **kwargs: object
    ) -> None:
        candidate = Path(path)
        if candidate.name.startswith(".theory-first-backup-"):
            raise KeyboardInterrupt
        real_rmtree(candidate, *args, **kwargs)

    monkeypatch.setattr(installer_module.shutil, "rmtree", interrupt_backup_cleanup)

    with pytest.raises(InstallError, match="installation was committed") as caught:
        install_suite(target, force=True)

    assert "installed skills are active" in str(caught.value)
    assert {path.name for path in target.iterdir()} == set(EXPECTED_SKILLS)
    assert not (target / "theory-first" / "user-content.txt").exists()
    backups = tuple(tmp_path.glob(".theory-first-backup-*"))
    assert len(backups) == 1
    assert (
        backups[0] / "theory-first" / "user-content.txt"
    ).read_text(encoding="utf-8") == "precious"
    assert str(backups[0]) in str(caught.value)
    assert not tuple(tmp_path.glob(".theory-first-*.lock"))


def test_post_commit_cleanup_error_reports_active_install(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "skills"
    real_rmtree = shutil.rmtree

    def fail_backup_cleanup(
        path: str | os.PathLike[str], *args: object, **kwargs: object
    ) -> None:
        candidate = Path(path)
        if candidate.name.startswith(".theory-first-backup-"):
            raise PermissionError("injected cleanup failure")
        real_rmtree(candidate, *args, **kwargs)

    monkeypatch.setattr(installer_module.shutil, "rmtree", fail_backup_cleanup)

    with pytest.raises(InstallError, match="installation was committed") as caught:
        install_suite(target)

    assert "installed skills are active" in str(caught.value)
    assert {path.name for path in target.iterdir()} == set(EXPECTED_SKILLS)
    assert tuple(tmp_path.glob(".theory-first-backup-*"))
    assert not tuple(tmp_path.glob(".theory-first-*.lock"))


def test_incomplete_rollback_preserves_backup_and_recovery_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "skills"
    _seed_stale_skill(target, "precious")
    real_rename = os.rename
    real_unlink = Path.unlink

    def fail_install_and_restore(
        source: str | os.PathLike[str], destination: str | os.PathLike[str]
    ) -> None:
        source_path = Path(source)
        destination_path = Path(destination)
        if (
            destination_path == target / "theory-first"
            and source_path.parent.name.startswith(".theory-first-stage-")
        ):
            raise OSError("injected install failure")
        if (
            source_path.parent.name.startswith(".theory-first-backup-")
            and destination_path == target / "theory-first"
        ):
            raise OSError("injected restore failure")
        real_rename(source, destination)

    def fail_lock_cleanup(self: Path, *args: object, **kwargs: object) -> None:
        if self.name.startswith(".theory-first-") and self.suffix == ".lock":
            raise PermissionError("injected lock cleanup failure")
        real_unlink(self, *args, **kwargs)

    monkeypatch.setattr(
        installer_module.os, "rename", fail_install_and_restore
    )
    monkeypatch.setattr(Path, "unlink", fail_lock_cleanup)

    with pytest.raises(InstallError, match="rollback was incomplete") as caught:
        install_suite(target, force=True)

    assert "preserved recovery data under" in str(caught.value)
    backups = tuple(tmp_path.glob(".theory-first-backup-*"))
    assert len(backups) == 1
    assert (
        backups[0] / "theory-first" / "user-content.txt"
    ).read_text(encoding="utf-8") == "precious"
    if hasattr(caught.value, "__notes__"):
        assert "lock cleanup also failed" in "\n".join(caught.value.__notes__)


def test_regular_file_race_is_preserved_as_defense_in_depth(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "skills"
    raced_path = target / EXPECTED_SKILLS[0]
    real_rename = os.rename
    injected = False

    def race_before_rename(
        source: str | os.PathLike[str], destination: str | os.PathLike[str]
    ) -> None:
        nonlocal injected
        source_path = Path(source)
        destination_path = Path(destination)
        if (
            not injected
            and destination_path == raced_path
            and source_path.parent.name.startswith(".theory-first-stage-")
        ):
            injected = True
            raced_path.write_text("concurrent writer", encoding="utf-8")
        real_rename(source, destination)

    monkeypatch.setattr(installer_module.os, "rename", race_before_rename)

    with pytest.raises(OSError):
        install_suite(target)

    assert injected
    assert raced_path.read_text(encoding="utf-8") == "concurrent writer"
    assert {path.name for path in target.iterdir()} == {EXPECTED_SKILLS[0]}
    assert not tuple(tmp_path.glob(".theory-first-*"))


def test_rollback_preserves_a_committed_skill_modified_by_an_external_writer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "skills"
    first_skill, second_skill = EXPECTED_SKILLS[:2]
    real_rename = os.rename

    def modify_first_then_fail_second(
        source: str | os.PathLike[str], destination: str | os.PathLike[str]
    ) -> None:
        source_path = Path(source)
        destination_path = Path(destination)
        is_staged_install = source_path.parent.name.startswith(
            ".theory-first-stage-"
        )
        if is_staged_install and destination_path == target / first_skill:
            real_rename(source, destination)
            (destination_path / "external-writer.txt").write_text(
                "do not delete", encoding="utf-8"
            )
            return
        if is_staged_install and destination_path == target / second_skill:
            raise OSError("injected failure after external write")
        real_rename(source, destination)

    monkeypatch.setattr(
        installer_module.os, "rename", modify_first_then_fail_second
    )

    with pytest.raises(InstallError, match="rollback was incomplete") as caught:
        install_suite(target)

    marker = target / first_skill / "external-writer.txt"
    assert marker.read_text(encoding="utf-8") == "do not delete"
    assert "installed path content changed; preserved" in str(caught.value)
    assert tuple(tmp_path.glob(".theory-first-backup-*"))
    assert not tuple(tmp_path.glob(".theory-first-*.lock"))
