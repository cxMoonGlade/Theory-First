# Release checklist

Use this checklist before making a public tag or announcing an install command.

- [ ] Review `git status` and the full staged diff; confirm no papers, extracted text, private notes, credentials, absolute paths, or unrelated files are included.
- [ ] Run `python -m pip install -e '.[dev]'` in a clean environment and run `pytest`.
- [ ] Run the current Agent Skills and Codex validators on all seven skills, the Codex plugin validator, `claude plugin validate . --strict`, and `python scripts/sync_portable_resources.py --check`.
- [ ] Build the sdist and wheel with `python -m build`, run `python -m twine check dist/*`, and run `scripts/verify_python_distribution.py` against both artifacts.
- [ ] Install the wheel in a clean virtual environment; verify `theory-first --version`, all seven copied skills, conflict refusal, forced replacement, and Codex/Claude/OpenCode discovery paths.
- [ ] Test a local marketplace and plugin install in an isolated `CODEX_HOME`.
- [ ] Create the intended GitHub repository, push the reviewed commit, and verify the manifest, privacy-policy, and README URLs.
- [ ] Enable GitHub private vulnerability reporting before inviting external users.
- [ ] Test `codex plugin marketplace add cxMoonGlade/Theory-First` and `codex plugin add theory-first@theory-first` from the published source.
- [ ] Test `claude plugin marketplace add cxMoonGlade/Theory-First` and `claude plugin install theory-first@theory-first` in an isolated Claude configuration.
- [ ] Test a clean `npx skills add --skill '*'` installation for OpenCode; verify all seven skills are discovered together and every referenced resource remains inside its own skill directory.
- [ ] Re-run the five positive, three negative, and parent/child collision cases; append the model/host/date and outcomes to the evaluation report.
- [ ] Pin a release tag or commit in reproducibility-sensitive installation instructions.
- [ ] Attach the exact checked wheel and sdist to the GitHub release, then repeat the documented remote `pip install` command and an isolated host install.
- [ ] Confirm the MIT license, BSD-3-Clause `pypdf` notice, and conceptual acknowledgements are current.

Do not mark a release complete merely because local tests pass. Remote URLs, installation, private security reporting, and the public artifact boundary must also be verified.
