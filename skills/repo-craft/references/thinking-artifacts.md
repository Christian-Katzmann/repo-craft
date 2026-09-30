# Thinking artifacts

Keep documents only when they answer a real question absent nearby. Apply the [three tests](tests-and-proofs.md), without quotas.

| Candidate | Earns its place when | Avoid |
| --- | --- | --- |
| Decision record | A consequential alternative and its reason will matter later | Invented deliberation or logs of routine edits |
| Rejected decision | A tempting feature was deliberately omitted | Treating every absent feature as deliberate |
| Architecture note | A non-obvious boundary or transformation needs explanation | Restating the tree |
| Limitations | Known constraints affect whether someone should use this | Generic disclaimers |
| Failure modes | Specific triggers, consequences and recovery are known | Hypothetical incidents presented as observations |
| Agent instructions | Important commands or fragile areas cannot be inferred cheaply | Boilerplate or inferred human authorship |
| Contribution guide | Contributors need instructions absent from first use | Irrelevant template sections |
| Security reporting note | A relevant channel and real policy exist | Invented response promises |
| Changelog | Real changes affect existing users | Fabricated release history |
| Design note | Repeated choices need a regeneration process | Presenting taste as universal |

For each keep, state reader, decision and source evidence. A paragraph in an existing document is often enough. Generated assistance is acceptable when facts are checked against the repository; “handwritten” is no quality guarantee.

Do not manufacture an origin story or private rationale. If code does not establish why a choice was made, label the explanation as inference and verify it where possible.
