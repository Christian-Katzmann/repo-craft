# Host constraints and studied examples

Use primary documentation for behavior and current repositories for taste. Observations checked on 2026-09-30 can change. Adapt patterns instead of copying templates or artwork.

## GitHub's surface

GitHub selects a README from .github, root, then docs. It provides a heading outline and branch-aware relative links, and truncates content beyond 500 KiB. See [GitHub's README documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).

Use supported Markdown and limited HTML. Do not promise custom CSS or arbitrary fonts in a README. A picture element can provide theme variants with prefers-color-scheme and an img fallback. A single image that works in both themes costs less to maintain. See [GitHub formatting](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/result-dark.png">
  <img src="docs/result-light.png" alt="Synthetic run: three candidates with source evidence">
</picture>
```

Paths depend on the selected README's directory. Host sanitization, fonts, chrome and theme can differ from a local preview. Source line counts do not measure a viewport. Record local-preview checks separately from actual GitHub checks.

## Three different openings

| Example | Observed pattern | Lesson to adapt | Cost to consider |
| --- | --- | --- | --- |
| [Glow](https://github.com/charmbracelet/glow) | Plain purpose, strong identity, terminal result, installation choices | Make a CLI's output recognizable and preserve copyable commands | Art and badges push first use down; signals can become stale |
| [DuckDB](https://github.com/duckdb/duckdb) | Compact overview with routes to documentation, installation and development | Route infrastructure readers to the appropriate depth | Links alone can leave newcomers without a local example |
| [Excalidraw](https://github.com/excalidraw/excalidraw) | Visual result, live product link, editor package/application distinction | Show the artifact and clarify which component the repository offers | Captures and feature lists must remain current and legible |

Retain URLs and retrieval date in research evidence. Distinguish inspected Markdown, host-rendered observation and inference. A small CLI and a visual workspace should not get identical layouts because both have READMEs.
