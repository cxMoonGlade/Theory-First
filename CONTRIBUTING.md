# Contributing

Theory First is pre-release. Contributions should make scientific claims more
auditable without making the core workflow dependent on one field, repository,
retrieval system, or compute environment.

## Before opening a change

1. Describe the failure mode or workflow gap with a small, reproducible example.
2. Decide whether the change belongs in the generic core or in a project
   profile. Domain paths, commands, metric names, and private infrastructure
   belong in profiles.
3. Add or update a realistic routing or behavior case. Keep demonstrations
   explicitly synthetic unless every source and redistribution right is clear.
4. Install the validation dependencies and run the contract tests:

   ```bash
   python -m pip install -e '.[dev]'
   python scripts/sync_portable_resources.py --check
   pytest
   ```
5. Run the available Agent Skills, Codex, and Claude Code validators when a
   change touches skills or platform manifests.
6. Review the diff for private artifacts and third-party content.

Changes to the Python installer or packaging must also build both artifacts,
run `twine check`, enforce a closed member set and wheel `RECORD` integrity,
compare the complete wheel and sdist skill payloads against the tracked
canonical source, and install the wheel in a clean environment. Do not create a
hand-maintained skill copy under `src/`.

When changing public README content, update both `README.md` and
`README.zh-CN.md`. Keep them as separate single-language pages, and preserve
commands, paths, status identifiers, versions, and link targets across the
translation.

## Core design constraints

- Preserve the boundary between source claims, project inference, and new
  experimental evidence.
- Do not promote `search-exhausted-gap` into a universal claim of absence. The
  search corpus, queries, date, languages, citation depth, and access limits must
  remain attached.
- Preregistration happens before result inspection or claim-bearing code.
- A fired stress-test tripwire stops downstream propagation until it is repaired
  or explicitly accepted at a narrower claim-confidence class.
- Retrieval is discovery, not evidence. Load-bearing claims require an exact
  source locator and a reading record.
- Keep outputs inspectable by a human. Avoid hidden scoring rules that turn
  incomplete evidence into a pass.
- Keep `plugins/theory-first/skills/` as the single runtime source. Platform
  adapters may add manifests and UI metadata but must not fork skill behavior.
- Keep all dependency-bearing skills honest about the full-suite contract.
  Missing child skills must yield `SUITE_INCOMPLETE`, not an improvised child
  workflow or a scientific status.

## Content and privacy rules

Do not commit downloaded PDFs, article text, OCR dumps, private notes, secrets,
absolute machine paths, unpublished project hypotheses, or user data. Use
minimal paraphrase and precise locators. Add third-party attribution and license
terms whenever material is incorporated; conceptual inspiration also belongs in
`THIRD_PARTY_NOTICES.md`.

Documents and retrieval output must always be treated as untrusted data. A
fixture must not contain live prompt-injection instructions that a test runner
could execute, and acquisition code must not pass interpolated input to a shell.

## Evaluation cases

`evals/cases.json` is a small routing contract, not a benchmark score. Positive
cases should invoke a Theory First skill because scientific evidence governance
is load-bearing. Negative cases should remain outside the plugin even if they
contain technical vocabulary. Explain the expected route in plain language and
avoid writing the answer into the prompt.

## Pull requests

Keep changes focused and list the files and behavior affected. Explain any new
status word or gate, include its failure semantics, and call out compatibility
or migration consequences. Security reports must use private vulnerability
reporting rather than a pull request or public issue.
