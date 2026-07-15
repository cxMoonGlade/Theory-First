# Security policy

## Reporting a vulnerability

After publication, use GitHub private vulnerability reporting for this repository. The maintainer must enable it before inviting external users. Do not
open a public issue containing an exploit, a private source URL, credentials,
research data, or a path that reveals a sensitive local environment.

Include the affected version or commit, the smallest safe reproduction, the
expected boundary, and the observed impact. Remove paper contents, tokens, and
personally identifying data from the report.

## Trust boundary

Papers, webpages, bibliographic metadata, PDF annotations, OCR output, local
retrieval results, and project notes are untrusted data. They can contain prompt
injection, misleading commands, hostile links, malformed documents, or text
that only looks like a project instruction.

The workflow must therefore preserve these rules:

- never execute commands, code, links, or tool instructions found inside a
  source;
- pass downloader arguments as structured values, never through an interpolated
  shell command;
- constrain network acquisition to the source the user requested and reject
  unexpected redirects or URL schemes;
- cap download size, parsing work, and page count before processing an
  unfamiliar document;
- write downloads atomically to a private cache or an explicit destination and
  avoid logging full text or absolute local paths by default;
- copy validated local source bytes into private staging and verify the digest
  again before parsing;
- treat retrieved passages as discovery leads until a primary source and exact
  locator have been checked;
- keep credentials and access tokens outside prompts, profiles, reading notes,
  fixtures, and logs.

Sandboxing and host permissions remain part of the security boundary. Use the
narrowest filesystem and network permissions that can complete the task.

## Supported versions

This project is pre-release. Until a stable release policy is published, only
the current default branch is eligible for security fixes.

## Not a security guarantee

The skills organize evidence and reduce predictable workflow errors; they do
not prove that a source, model output, experiment, or scientific conclusion is
safe or correct. Human review remains required for consequential decisions.
