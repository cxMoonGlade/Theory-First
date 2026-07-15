# Release checklist

Use this checklist before making a public tag or announcing an install command.

- [ ] Review `git status` and the full staged diff; confirm no papers, extracted text, private notes, credentials, absolute paths, or unrelated files are included.
- [ ] Run `python -m pip install -e '.[dev]'` in a clean environment and run `pytest`.
- [ ] Run the current Codex skill validator on all seven skills and the plugin validator on `plugins/theory-first`.
- [ ] Test a local marketplace and plugin install in an isolated `CODEX_HOME`.
- [ ] Create the intended GitHub repository, push the reviewed commit, and verify the manifest, privacy-policy, and README URLs.
- [ ] Enable GitHub private vulnerability reporting before inviting external users.
- [ ] Test `codex plugin marketplace add cxMoonGlade/Theory-First` and `codex plugin add theory-first@theory-first` from the published source.
- [ ] Re-run the five positive, three negative, and parent/child collision cases; append the model/host/date and outcomes to the evaluation report.
- [ ] Pin a release tag or commit in reproducibility-sensitive installation instructions.
- [ ] Confirm the MIT license, BSD-3-Clause `pypdf` notice, and conceptual acknowledgements are current.

Do not mark a release complete merely because local tests pass. Remote URLs, installation, private security reporting, and the public artifact boundary must also be verified.
