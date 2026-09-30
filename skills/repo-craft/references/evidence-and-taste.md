# Evidence and taste

| Label | Meaning | Example |
| --- | --- | --- |
| Evidence | A reproducible observation with its scope | Seven badge patterns matched in the first 30 README lines. |
| Signal | A detector's incomplete interpretation | No status phrase matched. Inspect the README before calling its status missing. |
| Taste | A preference with a project-specific reason | Keep install and test badges; the others compete with the usage example. |
| Decision | What to change, keep, inspect or defer | Keep the existing status wording because its second sentence explains the limitation. |

An exact pattern count is observable. Its meaning is a heuristic. Badge counts do not measure trust; path counts do not establish who wrote an agent guide. Image dimensions do not prove working software.

Probe schema 2 names the first 30 source lines sourceWindow instead of topFold. It records the selected README and never claims a rendered check. Images include inline Markdown and literal HTML src/srcset, not every reference-style image or host transformation. Recognized README names are bounded; other formats/capitalization need manual inspection.

## Confirm or refute a signal

Read the relevant file or run a safe check. Record a repository-relative location and a short non-sensitive quotation or command result. Evidence can refute a false positive without changing the repository.

A detector may miss “The import path works; export is unfinished.” Record that sentence as an honest status statement and close the signal. Do not add a redundant heading to satisfy a pattern. A tracked environment file with deliberate fake values is evidence of a file, not evidence of a leaked credential.

Missing README, LICENSE, CI, hero or social image is an observation. Decide its consequence from intended use and actual constraints. Private analysis can finish without a public license; redistribution may need rights clarification. A text library may need no hero. No missing artifact is intrinsically a publication blocker.

## Scanner states and scope

The probe checks history and the working tree separately. History covers all local Git refs using `--all`; it does not discover inaccessible remote history. The directory scan covers uncommitted and ignored files visible to that scan. Shallow history prevents an overall clean conclusion.

The wrapper uses an explicit scanner configuration and bypasses project ignore files and inline allow-comments for this check. It does not rewrite those project files. No scanner configuration makes detection exhaustive.

| State | Meaning | Consequence |
| --- | --- | --- |
| clean | Success exit status, valid parsed empty JSON findings array, and required scope evidence agree. History also requires positive scanned-commit evidence. | Record scope and version. No detected pattern is not proof of absence. |
| findings | Findings exit status and valid nonempty JSON report agree. | Inspect privately; distinguish real exposure from fixture data. |
| error | Execution, report parsing, scope evidence or exit/report consistency failed. | Repair the cause and rerun; do not claim the check passed. |
| unavailable | Gitleaks was unavailable. | No scanner conclusion exists. A text search is not an equivalent fallback. |
| skipped | The scope could not be scanned, such as history with no commits. | State why; a clean directory scan does not make skipped history clean. |

The probe tests Gitleaks 8.30.1. It requests exit 7 for findings and exit 0 for clean; another exit, including 1, is an error. It validates finding records rather than accepting any JSON value. Unsupported scanner flags produce an error, not a silent legacy fallback. Read both scope states even when an overall finding takes precedence over another scope's error.

The probe's own exit 0 means it could produce a report, including reports with findings or errors. Never use that exit as the secret-check verdict.

Reports contain safe counts and fixed status descriptions, never raw finding payloads, secrets, README content or scanner logs. Errors can contain sensitive text, so investigate privately and summarize the cause.

Confirmed sensitive content blocks sharing that content. Continue unaffected local work. Do not rotate real credentials, rewrite history or delete data merely because a pattern matched. Establish exposure and the authorized remediation scope. Development fixtures use generated fake values only. See [publication](publication.md).

## Resolve taste honestly

State reader benefit and cost. A project reason can outweigh a preference: six badges may link six relevant supported platform builds. No edit is needed merely to conform to a preferred count, palette or document quota. Record the user's choice without turning it into a factual defect.
