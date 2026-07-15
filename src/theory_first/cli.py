from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .bundle import BundleError, EXPECTED_SKILLS, bundle_root
from .installer import (
    AGENTS,
    InstallError,
    install_suites,
    target_for,
    unique_targets,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="theory-first",
        description="Install the complete Theory First Agent Skills suite.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("list", help="List the seven bundled skill names.")
    commands.add_parser("path", help="Print the bundled skills directory.")

    install = commands.add_parser(
        "install", help="Copy all seven skills into one or more host discovery paths."
    )
    destination = install.add_mutually_exclusive_group(required=True)
    destination.add_argument(
        "--agent",
        choices=AGENTS,
        action="append",
        help="Host to configure; repeat to configure multiple hosts.",
    )
    destination.add_argument(
        "--target",
        type=Path,
        help="Explicit skills directory for another Agent Skills host.",
    )
    install.add_argument(
        "--scope", choices=("user", "project"), default="user"
    )
    install.add_argument(
        "--project",
        type=Path,
        help="Project root; required when --scope project is selected.",
    )
    install.add_argument(
        "--force",
        action="store_true",
        help="Replace existing filesystem paths for the seven bundled skills.",
    )
    install.add_argument(
        "--dry-run", action="store_true", help="Show targets without writing files."
    )
    return parser


def _targets(args: argparse.Namespace) -> tuple[Path, ...]:
    if args.target is not None:
        if args.scope != "user" or args.project is not None:
            raise InstallError("--target cannot be combined with --scope or --project")
        return (args.target.expanduser().resolve(),)

    assert args.agent
    agents = tuple(dict.fromkeys(args.agent))
    # OpenCode discovers the standard .agents and .claude skill roots too. A
    # custom CLAUDE_CONFIG_DIR is not one of those roots, so it cannot cover an
    # OpenCode request.
    opencode_is_covered = "codex" in agents
    if "claude-code" in agents:
        claude_target = target_for(
            "claude-code", scope=args.scope, project=args.project
        )
        if args.scope == "project":
            opencode_is_covered = True
        else:
            default_claude_target = (
                Path.home() / ".claude" / "skills"
            ).expanduser().resolve()
            opencode_is_covered = (
                opencode_is_covered or claude_target == default_claude_target
            )
    if "opencode" in agents and opencode_is_covered:
        agents = tuple(agent for agent in agents if agent != "opencode")
    paths = [
        target_for(agent, scope=args.scope, project=args.project)
        for agent in agents
    ]
    return unique_targets(paths)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            print("\n".join(EXPECTED_SKILLS))
            return 0
        if args.command == "path":
            print(bundle_root())
            return 0

        results = install_suites(
            _targets(args), force=args.force, dry_run=args.dry_run
        )
        for result in results:
            action = "would install" if result.dry_run else "installed"
            print(f"{action} {len(result.skills)} skills -> {result.target}")
        return 0
    except (BundleError, InstallError, OSError) as error:
        print(f"theory-first: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
