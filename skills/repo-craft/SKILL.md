---
name: repo-craft
description: Craft distinctive repository presentations and READMEs from real project evidence. Use for audits, compelling first-use examples, screenshots, diagrams, visual hierarchy, and rendered before/after review. Adapts to CLI, library, data and interface projects. Keeps commands reproducible, claims bounded, and publication separate from local preparation.
---

# Repo Craft

Make it easy for a stranger to understand this project, inspect a real result, and take the next useful step. Keep artifacts that explain something specific. An attractive capture may help, but appearance never proves correctness.

## Start from the project

Resolve `SKILL_DIR` to the directory containing this file, wherever the host installed it. All runtime files are bundled here. Required: Bash 3.2+, Python 3.9+, and Git. Gitleaks is optional for exploration; the bundled secret check was tested with 8.30.1. Discover available tools with `command -v`. Do not assume an account, renderer, second agent, or paid provider.

1. Read the user's scope and repository instructions. Note the audience, actual project state, and prior publication authorization.
2. Run `git -C "$REPO_DIR" status --short` and preserve unrelated work. Git determines the root; a linked worktree can have a `.git` file instead of a directory.
3. Save the probe outside the target tree, so the report does not change the working-tree scan:

```sh
PROBE_REPORT=$(mktemp)
bash "$SKILL_DIR/scripts/repo-probe.sh" "$REPO_DIR" > "$PROBE_REPORT"
```

Read [evidence and taste](references/evidence-and-taste.md) before interpreting the report. Exit 0 means a report was produced, not that publication is safe. Exit 1 means unusable input; exit 2 means invalid usage. Optional `--json` produces structured output. The probe neither executes project code nor publishes anything.

Read the README, relevant implementation, and one actual result before proposing additions. Check setup and verify commands before running them. If execution needs unavailable credentials or services, name what remains untested and continue locally checkable work.

## Compose before adding artifacts

Read [composition and rendered review](references/composition.md). Choose one primary reader, the decision they are making, and one first useful action. Write a short creative direction specific to this project: what deserves emphasis, the order of evidence, and what earns less space. Keep a baseline before editing. The probe's first 30 source lines are a sampling window, never a measured viewport.

Build a deliberate opening: project name, concrete purpose, material status, one convincing result, and a runnable next step. Their order depends on the project. A tiny CLI may lead with copyable input/output; a visual workspace may lead with a task screenshot; a library may lead with a working integration. [Host constraints and studied examples](references/host-and-examples.md) explain GitHub's actual surface and patterns to adapt.

Verify the smallest useful journey in a disposable copy. If a visual earns space, produce it, embed it and inspect the rendered README at wide and narrow widths and in light and dark themes where supported. Fix illegible captures, broken assets, delayed commands and misleading crops. Record exact widths, what was actually rendered, and host differences. A source diff, image brief or successful build is not a rendered check. If rendering is unavailable, complete the text and report that limit explicitly.

## Three tests for every candidate

1. **Specific judgment:** What decision about this project does the artifact help the reader make?
2. **Duplication:** Does something already answer that question?
3. **Upkeep:** Is the benefit worth keeping the artifact accurate when the project changes?

Fail any test and skip or simplify the candidate. For an image, ask whether it could be swapped with a competitor's image without losing meaning. A generic illustration fails as project proof. These are judgments with reasons, not a readiness score. See [tests and proofs](references/tests-and-proofs.md).

## Seven questions, not seven required files

1. **What can be shared?** Inspect scan states and relevant files for sensitive content and licensing constraints. A detector hit needs inspection; an unavailable scan is unknown. Confirmed exposure can block a specific publication while safe local preparation continues. Use [evidence and taste](references/evidence-and-taste.md).
2. **What is this for?** Write a plain positioning sentence from what works now, plus an honest status statement. Suggest name, description or topic changes only when they clarify the project. Do not silently modify an account.
3. **What should visitors see first?** The README opening answers purpose, current state, where to inspect a result, and fastest next step. Explain a likely misunderstanding if one exists. A usage example may do more than a hero. Use [tests and proofs](references/tests-and-proofs.md).
4. **What visual would teach something?** Capture an actual interface, terminal output or result comparison with labeled synthetic data. Preserve its inputs and reproduction steps. Caption the claim narrowly and include accessible text. Use [visual craft](references/visual-craft.md) and [producer handoff](references/producer-handoff.md). Separately decide whether a [website](references/repository-vs-website.md) serves a useful audience or interaction.
5. **Can readers reproduce it?** Follow first use from a clean disposable copy where feasible. Record real commands and outcomes. Describe missing configuration and external requirements. Add a configuration example only where configuration exists. Never invent CI success or a working demo.
6. **Which supporting records matter?** Consider decision records, architecture notes, limitations, contribution guides or agent instructions only when they capture knowledge absent nearby. Ground them in real paths, commands and tradeoffs. Authorship cannot be inferred from prose style. Use [thinking artifacts](references/thinking-artifacts.md).
7. **What is ready to release?** Verify changed links, selected assets, license/notice preservation and documented commands. Prepare concrete local assets and an exact list of pending external operations. Follow the single [publication rule](references/publication.md), honoring prior authorization without requesting it again.

Use [restraint examples](references/rejections.md) for repetitive or decorative additions. The user's product judgment can override taste preferences; record the reason. Unsupported factual claims are not taste overrides.

## Finish

Use the [report format](references/report-format.md): observations, unresolved checks, consequential keep/skip decisions, changed files, commands and actual results, pending external operations. For presentation changes retain before/after files and rendered evidence, or state why rendering was unavailable. No readiness score.

Completion follows the requested scope: the README accurately explains the project, kept artifacts pass the three tests, and the worked result is reproducible or explicitly limited. Missing optional images or a Pages site are not failures. A clean scan is a result for its recorded scope, not proof that no secrets exist.

Remove temporary reports after retaining safe evidence. Stop and verify cleanup of every process you started.
