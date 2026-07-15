# Privacy

Theory First is designed for local, user-controlled research workflows.

## Data handled by the plugin

Depending on the task, the skills may read project documentation, source code,
local literature indexes, papers the user is authorized to access, and
user-supplied scientific claims. They may produce reading notes, evidence
ledgers, search records, preregistrations, and stress-test reports.

Those artifacts should be stored in a local workspace, an access-controlled
project location, or a private cache selected by the user. Do not place private
research artifacts inside this plugin repository.

## Telemetry and network access

The plugin code in this repository has no telemetry endpoint and sends no
analytics. Landscape mapping and literature closure can send minimized search
queries and source identifiers to configured search providers, scholarly
indexes, publisher sites, or source repositories when the task authorizes
external retrieval and the host permits it. The workflow should name the first
external destination, strip confidential project terms when possible, and
honor a local-only boundary. Downloaded artifacts and their cleanup remain the
user's responsibility unless a marker-owned cache is explicitly cleaned.

The host application, model provider, operating system, and any configured
search or storage services are separate processors governed by their own
settings and terms.

## Repository contents

The public repository does not include downloaded papers, transcripts,
extracted full text, private reading notes, unpublished hypotheses, credentials,
or machine-specific absolute paths. Contributors must use synthetic or openly
redistributable fixtures and remove embedded document metadata before
submission.

## Minimization

Record only what an audit needs: a paraphrased claim, a precise locator, source
identity, search boundary, and the reasoning that connects evidence to the
project claim. Avoid copying long passages. When sharing a report, review it for
paths, usernames, tokens, unpublished claims, and restricted source text.
