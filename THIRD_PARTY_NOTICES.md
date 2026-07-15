# Third-party notices

Theory First is original work. It does not vendor papers, transcripts,
extracted full text, source code, or skill text from the works below. Their
inclusion here records conceptual provenance; it does not imply endorsement,
affiliation, or transfer of copyright.

## Research-practice influences

- Richard Hamming, *You and Your Research* (1986 lecture; a transcript is
  available from [Gwern Branwen's archive](https://gwern.net/doc/science/1986-hamming)).
  Its discussion of choosing consequential problems informed the workflow's
  insistence on stating why a question matters before investing in it.
- Michael Nielsen, *Principles of Effective Research*
  ([author's article](https://michaelnielsen.org/blog/principles-of-effective-research/)).
  Its research-strategy framing informed the separation between broad
  landscape mapping and narrow, load-bearing close reading.

No article wording is reproduced here. Users are responsible for obtaining and
using source material under the applicable copyright and access terms.

## Agent-workflow influence

Matt Pocock's public [skills repository](https://github.com/mattpocock/skills),
including its historical `zoom-out` workflow, helped motivate an explicit “map
before narrowing” stage. That upstream repository is published under the
[MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE).
Theory First ships an independently written `map-research-landscape` workflow;
it does not redistribute the upstream skill or its code.

## Interoperability

The skill directories follow the open
[Agent Skills specification](https://agentskills.io/specification). Its
reference implementation is published by the
[Agent Skills project](https://github.com/agentskills/agentskills) under
Apache-2.0; its documentation states CC-BY-4.0 terms. Theory First does not
copy the specification text or reference implementation.

The optional cross-platform installation commands use Vercel Labs'
[`skills` CLI](https://github.com/vercel-labs/skills). It is fetched and run
separately by the user and is not vendored or imported by this repository;
its upstream repository and package terms apply.

## Runtime dependency

The optional bounded-text extractor uses
[`pypdf`](https://github.com/py-pdf/pypdf), distributed under the
[BSD 3-Clause License](https://github.com/py-pdf/pypdf/blob/main/LICENSE). The
library is installed separately and is not vendored in this repository.

If a future contribution incorporates third-party material, it must preserve
the relevant license, attribution, and file-level notices and must update this
document before release.
