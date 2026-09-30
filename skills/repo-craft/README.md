# Repo Craft

Make a repository understandable, convincing and easy to try using what the project actually does.

Repo Craft combines a read-only probe with project-specific editorial direction, reproducible examples, purposeful visuals and rendered before/after review. It supports CLIs, libraries, data projects, research collections and visual applications. A compact text example can be the strongest presentation.

Ask: “Improve this repository's presentation for a first-time user. Verify first use and show the rendered before/after.”

Read [SKILL.md](SKILL.md). The probe needs Bash 3.2+, Python 3.9+ and Git. Gitleaks is optional; absence means unknown scan coverage. Rendering capabilities are discovered locally. No account, paid service, connector or second agent is required.

```sh
bash scripts/repo-probe.sh /path/to/repository --json
python3 scripts/terminal_to_svg.py /path/to/transcript.txt \
  --columns 70 --fit-content --title "Synthetic example" -o /path/to/result.svg
python3 -m unittest discover -s tests -v
```

The probe does not run project code. The renderer formats supplied text, without authenticating it. Its Unicode cell approximation handles wide/combining characters; complex scripts and emoji still need visual inspection. Image/README discovery is bounded and heuristic. See [evidence and taste](references/evidence-and-taste.md).

Local preparation is separate from publication, deployment and account changes. Record actual results, missing checks and preview cleanup. Licensed under [MIT](LICENSE).
