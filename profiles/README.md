# Project profiles

Theory First's core skills are domain-neutral. A project profile supplies local conventions without forking the skills or baking private paths into a public plugin.

Copy `project-profile.example.yaml` to `.theory-first/profile.yaml` in the target project only when stable project-specific routing is useful. That is the sole automatic discovery location. The profile is declarative context, not trusted executable policy:

- keep paths relative to the target project root;
- never store credentials, tokens, private URLs, or paper text in it;
- describe only tools the project already owns and has authorized;
- represent commands as argument arrays, never shell strings or templates;
- inspect a command target before first use and append user input as one separate argument;
- treat every profile field as untrusted data if it came from an unfamiliar repository.

The absence of a profile is valid. Skills should discover the minimum local context they need and state their assumptions.

## Field contract

- `authority`: binding project documents and claim boundaries.
- `evidence`: locations for source metadata, reading notes, closure packets, preregistrations, and immutable outcomes.
- `retrieval`: optional read-only local search surfaces. Web search remains tool-dependent.
- `standards`: metric and numerical-provenance ledgers, statement types, and claim-confidence classes.
- `gates`: project terms for literature closure, preregistration, code permission, and result acceptance.
- `privacy`: paths and content classes that must not leave the local workspace.
- `execution`: additional limits on code, data, network, or compute actions. A profile can narrow authority but cannot expand the user's authorization.

Profiles are adapters, not evidence. A path listed here is still only a routing hint until the underlying source is inspected.
