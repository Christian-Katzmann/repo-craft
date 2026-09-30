# Repo Craft

![Repo Craft](assets/icon.png)

Help people understand and try a repository through clear READMEs, verified first-use examples and truthful visual evidence.

## Install

Use the portable plugin ZIP with a compatible local skill host. The package contains `plugin.json` and `skills/repo-craft/SKILL.md`. Follow your host’s plugin installation instructions. Directory listing and OpenAI review are not yet complete.

Requires local Python, Bash and Git. Gitleaks and browser tools are optional; missing tools and unverified outcomes must remain visible.

## Use

Ask your coding assistant: “Audit this repository README and suggest a clearer first-use journey.” Repo Craft adapts to libraries, command-line tools, data projects and interfaces. It includes a read-only repository probe and a deterministic terminal-to-SVG renderer.

Start with the [skill guide](skills/repo-craft/README.md). Verify a small real workflow, use actual output and distinguish source inspection from rendered evidence. Findings are heuristics, not a security certification. Publication, deployment and remote changes require authorization.

## Privacy and license

The bundled helpers do not collect telemetry or send network requests. Reports and screenshots can contain repository data; review before sharing. Your coding host and any separately invoked services have their own privacy controls. See [privacy policy](PRIVACY.md). Private support: christian@katzmann.dk; do not send credentials or private repository contents.

Copyright © 2026 Christian Katzmann. Licensed under [MIT](LICENSE).
