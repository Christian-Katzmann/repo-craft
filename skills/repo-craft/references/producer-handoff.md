# Producer handoff

Name inputs, required evidence and the deliverable, without relying on a private path, account, plugin or orchestration command.

## Discover capability

Inspect available tool descriptions and local executables. Common capabilities are transcript rendering, SVG rasterization, browser capture and video composition. Tool presence does not establish authentication, formats or permission to spend money.

Prefer an existing local capability. The bundled [terminal renderer](../scripts/terminal_to_svg.py) needs only Python 3.9+. An available browser or SVG rasterizer can produce a raster when required. No separate agent or design service is mandatory.

If a capability is absent, write the brief and record “not rendered” with the missing capability. Use an adequate simpler artifact when possible. Never claim a brief is a finished image, silently drop a promised visual, or start an interactive login or purchase.

## Portable brief

Use repository-relative paths and include:

- Reader question the artifact must answer.
- Actual input, command or interaction, and captured output. Label synthetic data.
- Narrow claim and limits of the evidence.
- Result to emphasize, necessary context, caption and alt text.
- Local output path, format and intended displayed size.
- Reproduction command or capture steps, environment and expected result.
- Completion evidence: output file, render check, source, omissions and missing capabilities.

Reuse project assets. The same brief should be usable by an available tool or a person.

## Terminal example

Save real commands prefixed with `$ ` and actual output in `transcript.txt`. Keep the full transcript; redact sensitive content before rendering and mark any redaction. Never distribute credential-bearing evidence.

From the target repository, with `SKILL_DIR` resolved to this installed skill:

```sh
mkdir -p design/screenshots
python3 "$SKILL_DIR/scripts/terminal_to_svg.py" transcript.txt \
  --columns 70 --fit-content --title "Planner result" -o design/screenshots/01-plan.svg
```

Run the underlying command separately and compare the transcript to its result. Inspect the SVG at its embedded size, including narrow screens. The capture uses a neutral title strip. Keep text-only output if scaling hurts readability. Complex scripts and emoji require font/render inspection.

An optional poster:

```sh
mkdir -p design/social
python3 "$SKILL_DIR/scripts/terminal_to_svg.py" transcript.txt \
  --poster --name "Fairshare" \
  --positioning "Plan household tasks within each person's weekly limit." \
  -o design/social/social-preview.svg
```

Posters have limited space. Use a short complete result or an explicitly labeled excerpt linked to the full transcript. Do not hide omitted failures. Rasterize only if needed, using a discovered capability, then inspect the actual raster at its intended size.

## Return the result

Return local output, input, command, dimensions, visual inspection result and limits. The caller checks files and references before embedding. Stop and verify cleanup of rendering processes. Uploads and account changes follow [publication](publication.md); producing an asset does not authorize distribution.
