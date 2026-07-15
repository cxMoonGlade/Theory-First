from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "theory-first"
SKILLS = PLUGIN / "skills"
VERSION = "0.2.0"
EXPECTED_SKILLS = {
    "theory-first",
    "theory-fix",
    "close-literature",
    "deep-read-paper",
    "preregister-claim",
    "stress-test-claim",
    "map-research-landscape",
}
REQUIRED_CHILDREN = {
    "theory-first": {
        "map-research-landscape",
        "close-literature",
        "deep-read-paper",
        "preregister-claim",
    },
    "theory-fix": {
        "close-literature",
        "deep-read-paper",
        "stress-test-claim",
    },
    "close-literature": {"deep-read-paper"},
}


def _frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"missing frontmatter: {path}"
    _, raw, body = text.split("---", 2)
    return yaml.safe_load(raw), body


def test_skill_set_and_frontmatter_contract() -> None:
    assert {p.name for p in SKILLS.iterdir() if p.is_dir()} == EXPECTED_SKILLS

    for skill_name in EXPECTED_SKILLS:
        metadata, body = _frontmatter(SKILLS / skill_name / "SKILL.md")
        assert set(metadata) == {"name", "description"}
        assert metadata["name"] == skill_name
        description = metadata["description"]
        assert isinstance(description, str)
        assert 80 <= len(description) <= 1024
        assert "TODO" not in description
        assert body.strip()


def test_skill_resource_links_resolve() -> None:
    resource_link = re.compile(r"`((?:references|scripts)/[^`]+)`")
    for skill_name in EXPECTED_SKILLS:
        skill_dir = SKILLS / skill_name
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for relative in resource_link.findall(text):
            assert (skill_dir / relative).is_file(), (
                f"broken resource link in {skill_name}: {relative}"
            )


def test_skill_markdown_links_stay_inside_the_portable_skill() -> None:
    markdown_link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for skill_name in EXPECTED_SKILLS:
        skill_dir = SKILLS / skill_name
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for target in markdown_link.findall(text):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            resolved = (skill_dir / relative).resolve()
            assert resolved.is_relative_to(skill_dir.resolve()), (
                f"portable skill link escapes {skill_name}: {target}"
            )
            assert resolved.is_file(), f"broken link in {skill_name}: {target}"


def test_portable_status_models_match_the_canonical_table() -> None:
    canonical = (PLUGIN / "STATUS_MODEL.md").read_bytes()
    for skill_name in {"theory-first", "theory-fix"}:
        portable = SKILLS / skill_name / "references" / "status-model.md"
        assert portable.read_bytes() == canonical


def test_dependency_bearing_skills_require_the_complete_suite() -> None:
    status_model = (PLUGIN / "STATUS_MODEL.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "SUITE_INCOMPLETE" in status_model
    assert "not supported standalone installs" in readme
    portable_install_commands = [
        line for line in readme.splitlines() if line.startswith("npx skills")
    ]
    assert portable_install_commands
    assert all("--skill '*'" in line for line in portable_install_commands)

    for parent, children in REQUIRED_CHILDREN.items():
        text = (SKILLS / parent / "SKILL.md").read_text(encoding="utf-8")
        assert "SUITE_INCOMPLETE" in text
        assert re.search(r"complete seven-skill Theory\s+First suite", text)
        for child in children:
            assert child in EXPECTED_SKILLS
            assert f"`{child}`" in text


def test_skill_ui_metadata_matches_directory() -> None:
    for skill_name in EXPECTED_SKILLS:
        metadata = yaml.safe_load(
            (SKILLS / skill_name / "agents" / "openai.yaml").read_text(
                encoding="utf-8"
            )
        )["interface"]
        assert metadata["display_name"]
        assert 20 <= len(metadata["short_description"]) <= 80
        assert f"${skill_name}" in metadata["default_prompt"]


def test_public_skills_contain_no_private_project_residue() -> None:
    forbidden = {
        "absolute Linux home path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
        "absolute macOS home path": re.compile(r"/Users/[A-Za-z0-9._-]+/"),
        "absolute Windows home path": re.compile(
            r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\"
        ),
        "obsolete gap status": re.compile(r"confirmed-literature-gap"),
        "unsafe query placeholder": re.compile(r"\{query\}"),
        "generator placeholder": re.compile(r"\bTODO\b"),
    }
    corpus = "\n".join(
        path.read_text(encoding="utf-8")
        for path in SKILLS.rglob("*")
        if path.is_file() and path.suffix in {".md", ".yaml", ".py"}
    )
    for label, pattern in forbidden.items():
        assert not pattern.search(corpus), f"found {label} in public skills"


def test_plugin_and_marketplace_manifests() -> None:
    codex_plugin = json.loads(
        (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    claude_plugin = json.loads(
        (PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    codex_marketplace = json.loads(
        (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
            encoding="utf-8"
        )
    )
    claude_marketplace = json.loads(
        (ROOT / ".claude-plugin" / "marketplace.json").read_text(
            encoding="utf-8"
        )
    )

    common_fields = {
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
        "skills",
    }
    assert {field: codex_plugin[field] for field in common_fields} == {
        field: claude_plugin[field] for field in common_fields
    }
    assert codex_plugin["name"] == "theory-first"
    assert codex_plugin["version"] == VERSION
    assert codex_plugin["skills"] == "./skills/"
    assert claude_plugin["displayName"] == "Theory First"
    assert len(codex_plugin["interface"]["defaultPrompt"]) <= 3
    assert all(
        len(prompt) <= 128
        for prompt in codex_plugin["interface"]["defaultPrompt"]
    )

    codex_entry = codex_marketplace["plugins"][0]
    assert codex_entry["name"] == codex_plugin["name"]
    assert codex_entry["source"] == {
        "source": "local",
        "path": "./plugins/theory-first",
    }
    assert (ROOT / codex_entry["source"]["path"]).resolve() == PLUGIN.resolve()

    assert claude_marketplace["name"] == "theory-first"
    assert claude_marketplace["owner"]["name"] == "cxMoonGlade"
    claude_entry = claude_marketplace["plugins"][0]
    assert claude_entry == {
        "name": claude_plugin["name"],
        "source": "./plugins/theory-first",
    }
    assert (ROOT / claude_entry["source"]).resolve() == PLUGIN.resolve()


def test_release_version_is_synchronized() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    readmes = [
        (ROOT / name).read_text(encoding="utf-8")
        for name in ("README.md", "README.zh-CN.md")
    ]
    assert f'version = "{VERSION}"' in pyproject
    assert f"## {VERSION} " in changelog
    assert all(
        f"/tree/v{VERSION}/plugins/theory-first/skills" in readme
        for readme in readmes
    )


def test_public_installation_surfaces_are_documented() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required = {
        "codex plugin marketplace add cxMoonGlade/Theory-First",
        "claude plugin marketplace add cxMoonGlade/Theory-First",
        "--agent opencode",
        "Agent Skills",
    }
    assert all(item in readme for item in required)


def test_readmes_are_separate_reciprocal_language_pages() -> None:
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    assert [line for line in english.splitlines() if line][:2] == [
        "# Theory First",
        "English | [简体中文](README.zh-CN.md)",
    ]
    assert [line for line in chinese.splitlines() if line][:2] == [
        "# Theory First",
        "[English](README.md) | 简体中文",
    ]
    assert english.count("(README.zh-CN.md)") == 1
    assert chinese.count("(README.md)") == 1
    assert "## Workflow" in english
    assert "## 工作流程" in chinese
    assert "## 工作流程" not in english
    assert "## Workflow" not in chinese

    han = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
    assert not han.search(english.replace("简体中文", "", 1))

    chinese_prose = re.sub(r"```.*?```", "", chinese, flags=re.DOTALL)
    chinese_prose = re.sub(r"`[^`\n]*`", "", chinese_prose)
    chinese_prose = re.sub(r"\]\([^)]+\)", "]", chinese_prose)
    long_english_blocks = [
        block
        for raw_block in re.split(r"\n\s*\n", chinese_prose)
        if (
            block := re.sub(r"\s+", " ", raw_block).strip()
        )
        and len(re.sub(r"\W+", "", block)) >= 40
        and not han.search(block)
    ]
    assert long_english_blocks == []

    english_heading_levels = re.findall(r"^(#{2,3}) ", english, re.MULTILINE)
    chinese_heading_levels = re.findall(r"^(#{2,3}) ", chinese, re.MULTILINE)
    assert english_heading_levels == chinese_heading_levels

    english_bash = re.findall(r"```bash\n(.*?)\n```", english, re.DOTALL)
    chinese_bash = re.findall(r"```bash\n(.*?)\n```", chinese, re.DOTALL)
    assert english_bash == chinese_bash

    required_commands = {
        "npx skills add cxMoonGlade/Theory-First --skill '*' --agent opencode --global --yes",
        "npx skills add cxMoonGlade/Theory-First --skill '*' --agent claude-code --agent opencode --agent codex --global --yes",
        f"npx skills@1.5.17 add https://github.com/cxMoonGlade/Theory-First/tree/v{VERSION}/plugins/theory-first/skills --skill '*' --agent opencode --global --copy --yes",
        "codex plugin marketplace add cxMoonGlade/Theory-First",
        "codex plugin add theory-first@theory-first",
        "claude plugin marketplace add cxMoonGlade/Theory-First",
        "claude plugin install theory-first@theory-first",
    }
    for document in (english, chinese):
        assert all(command in document for command in required_commands)

    markdown_link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    language_pages = {"README.md", "README.zh-CN.md"}
    english_targets = sorted(
        target
        for target in markdown_link.findall(english)
        if target not in language_pages
    )
    chinese_targets = sorted(
        target
        for target in markdown_link.findall(chinese)
        if target not in language_pages
    )
    assert english_targets == chinese_targets

    identifiers = {
        "CODE_PERMITTED",
        "CODE_BLOCKED",
        "SUITE_INCOMPLETE",
        "search-exhausted-gap",
        "ACCEPT_WITH_CLASS",
        "REPAIR",
        "STOP",
        "REOPEN_EVIDENCE",
        "v0.2.0",
        "plugins/theory-first/skills/",
    }
    assert all(identifier in english for identifier in identifiers)
    assert all(identifier in chinese for identifier in identifiers)


def test_project_profile_uses_declarative_safe_argv() -> None:
    public_example = ROOT / "profiles" / "project-profile.example.yaml"
    installed_example = (
        SKILLS
        / "theory-first"
        / "references"
        / "project-profile.example.yaml"
    )
    assert public_example.read_bytes() == installed_example.read_bytes()
    profile = yaml.safe_load(public_example.read_text(encoding="utf-8"))
    assert profile["schema_version"] == 1
    assert set(profile) == {
        "schema_version",
        "project",
        "authority",
        "evidence",
        "retrieval",
        "standards",
        "gates",
        "privacy",
        "execution",
    }
    assert set(profile["standards"]["statement_types"]) == {
        "exact",
        "registered_prediction",
        "heuristic_gate",
    }
    assert profile["standards"]["claim_confidence_classes"]
    for command in profile["retrieval"]["commands"]:
        assert command["enabled"] is False
        assert isinstance(command["argv"], list)
        assert command["argv"]
        assert all(isinstance(arg, str) for arg in command["argv"])
        assert not any("{query}" in arg for arg in command["argv"])
        assert command["read_only"] is True


def test_routing_eval_balance() -> None:
    cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))[
        "cases"
    ]
    assert len(cases) == 8
    assert sum(case["should_trigger"] is True for case in cases) == 5
    assert sum(case["should_trigger"] is False for case in cases) == 3
    assert len({case["id"] for case in cases}) == len(cases)
    for case in cases:
        assert set(case) == {
            "id",
            "prompt",
            "should_trigger",
            "expected_skill",
            "rationale",
        }
        if case["should_trigger"]:
            assert case["expected_skill"] in EXPECTED_SKILLS
        else:
            assert case["expected_skill"] is None


def test_parent_child_collision_cases_are_explicit() -> None:
    cases = json.loads(
        (ROOT / "evals" / "collisions.json").read_text(encoding="utf-8")
    )["cases"]
    assert len(cases) >= 4
    assert len({case["id"] for case in cases}) == len(cases)
    for case in cases:
        assert set(case) == {
            "id",
            "prompt",
            "expected_skill",
            "must_not_route_directly_to",
            "rationale",
        }
        assert case["expected_skill"] in EXPECTED_SKILLS
        assert case["must_not_route_directly_to"] in EXPECTED_SKILLS
        assert case["expected_skill"] != case["must_not_route_directly_to"]


def test_no_research_full_text_or_pdf_is_bundled() -> None:
    forbidden_suffixes = {".pdf", ".html", ".txt"}
    generated_parts = {
        ".git",
        ".pytest_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "venv",
    }
    bundled = [
        path.relative_to(ROOT)
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in forbidden_suffixes
        and not generated_parts.intersection(path.parts)
        and not any(part.endswith(".egg-info") for part in path.parts)
    ]
    assert bundled == []


def test_relative_markdown_links_resolve() -> None:
    markdown_link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for document in ROOT.rglob("*.md"):
        for target in markdown_link.findall(document.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            assert (document.parent / relative).exists(), (
                f"broken link in {document.relative_to(ROOT)}: {target}"
            )


def test_status_model_covers_every_child_and_parent_outcome() -> None:
    status_model = (PLUGIN / "STATUS_MODEL.md").read_text(encoding="utf-8")
    required = {
        "AMBIGUOUS",
        "INFERENCE_ONLY",
        "SEARCH_EXHAUSTED_GAP",
        "CODE_BLOCKED",
        "CODE_PERMITTED",
        "PENDING",
        "REOPEN_EVIDENCE",
        "REPAIR",
        "STOP",
        "ACCEPT_WITH_CLASS",
        "SUITE_INCOMPLETE",
    }
    assert required.issubset(set(re.findall(r"[A-Z][A-Z_-]+", status_model)))
    assert "scientific-workflow clearance only" in status_model


def test_ci_actions_are_commit_pinned() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"
    )
    action_refs = re.findall(r"uses:\s+[^@\s]+@([^\s#]+)", workflow)
    assert action_refs
    assert all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in action_refs)
