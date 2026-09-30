#!/usr/bin/env python3
"""Render a real terminal transcript as a deterministic SVG.

A transcript is a plain text file. Lines that start with "$ " are commands;
every other line is output, exactly as the program printed it. The SVG shows
that text in a terminal panel. Nothing is invented: if the transcript holds
what the command printed, the picture is an honest capture.

    python3 terminal_to_svg.py transcript.txt -o design/screenshots/01-run.svg
    python3 terminal_to_svg.py transcript.txt --poster --name Fairshare \
        --positioning "One sentence that says what the project is." \
        -o design/social/social-preview.svg

The default output is a capture sized to the text. --poster renders a
1280x640 social preview with three elements: the name, one positioning
sentence and the terminal panel. Output has no clock, no random values and no
external references, so the same transcript and options yield the same bytes.
Oversized posters fail unless --excerpt-lines explicitly requests a labeled
excerpt. No text is silently cropped. Tabs become four spaces and long lines
wrap; ANSI escape sequences are unsupported. Only the standard library is used.
"""
from __future__ import annotations

import argparse
import sys
import unicodedata
from xml.sax.saxutils import escape, quoteattr

MONO = "Menlo, Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace"
SANS = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
SERIF = "Georgia, 'Times New Roman', 'Liberation Serif', serif"

THEMES = {
    "dark": {"panel": "#151b23", "text": "#e6edf3", "prompt": "#7ee787", "command": "#ffffff",
             "muted": "#a2adbb", "paper": "#0d1117", "ink": "#e6edf3"},
    "light": {"panel": "#f6f8fa", "text": "#24292f", "prompt": "#116329", "command": "#111417",
              "muted": "#57606a", "paper": "#ffffff", "ink": "#24292f"},
}

FONT_SIZE = 15
CHAR_WIDTH = 9.0
LINE_HEIGHT = 22
PADDING = 22
TITLE_BAR = 34


def cell_width(char: str) -> int:
    return 0 if unicodedata.combining(char) else (2 if unicodedata.east_asian_width(char) in ('W', 'F') else 1)


def display_width(text: str) -> int:
    return sum(cell_width(char) for char in text)


def wrap(line: str, columns: int) -> list[str]:
    parts, current, width = [], '', 0
    for char in line:
        cells = cell_width(char)
        if current and width + cells > columns:
            parts.append(current)
            current, width = '', 0
        current += char
        width += cells
    return parts + [current] if current or not parts else parts


def unsupported_control(char: str) -> bool:
    return unicodedata.category(char) in ('Cc', 'Cf')


def read_transcript(path: str, columns: int) -> list[tuple[str, str]]:
    if path == "-":
        raw = sys.stdin.read()
    else:
        with open(path, encoding="utf-8") as handle:
            raw = handle.read()
    if any(unsupported_control(char) and char not in "\n\r\t" for char in raw):
        raise ValueError("use plain text without ANSI escapes or control characters")
    rows: list[tuple[str, str]] = []
    for line in raw.removesuffix("\n").split("\n"):
        line = line.rstrip("\r").expandtabs(4)
        kind = "command" if line.startswith("$ ") else "output"
        text = line[2:] if kind == "command" else line
        for index, piece in enumerate(wrap(text, columns - 2 if kind == "command" else columns)):
            rows.append((kind if index == 0 else "continuation", piece))
    if not any(text.strip() for _, text in rows):
        raise SystemExit("terminal_to_svg: the transcript is empty")
    return rows


def panel(rows, columns, theme, x, y, title):
    colours = THEMES[theme]
    width = int(columns * CHAR_WIDTH + 2 * PADDING)
    height = int(TITLE_BAR + len(rows) * LINE_HEIGHT + 2 * PADDING)
    parts = [f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="10" fill="{colours["panel"]}"/>']
    if title:
        parts.append(f'<text x="{x + PADDING}" y="{y + 22}" font-family="{SANS}" '
                     f'font-size="12" fill="{colours["muted"]}">{escape(title)}</text>')
    text_y = y + TITLE_BAR + PADDING + FONT_SIZE
    for kind, text in rows:
        if kind == "command":
            parts.append(f'<text x="{x + PADDING}" y="{text_y}" xml:space="preserve" font-family="{MONO}" '
                         f'font-style="normal" font-size="{FONT_SIZE}" fill="{colours["prompt"]}">$ </text>')
            parts.append(f'<text x="{x + PADDING + 2 * CHAR_WIDTH:.0f}" y="{text_y}" xml:space="preserve" '
                         f'font-family="{MONO}" font-style="normal" font-weight="bold" font-size="{FONT_SIZE}" '
                         f'fill="{colours["command"]}">{escape(text)}</text>')
        elif text:
            parts.append(f'<text x="{x + PADDING}" y="{text_y}" xml:space="preserve" font-family="{MONO}" '
                         f'font-style="normal" font-size="{FONT_SIZE}" fill="{colours["text"]}">{escape(text)}</text>')
        text_y += LINE_HEIGHT
    return parts, width, height


def capture(rows, columns, theme, title):
    if display_width(title) > columns:
        raise ValueError("--title must fit within --columns")
    parts, width, height = panel(rows, columns, theme, 0, 0, title)
    body = "\n".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label={quoteattr(title or "terminal capture")}>\n'
            f'{body}\n</svg>\n')


def poster(rows, columns, theme, title, name, positioning, excerpt_lines=None):
    colours = THEMES[theme]
    width, height = 1280, 640
    panel_x = 80
    panel_y = 300
    max_rows = int((height - panel_y - 40 - TITLE_BAR - 2 * PADDING) // LINE_HEIGHT)
    if columns * CHAR_WIDTH + 2 * PADDING > width - 2 * panel_x:
        raise ValueError("poster width exceeds its canvas; use --columns 119 or fewer")
    if display_width(name) > 20:
        raise ValueError("poster name exceeds 20 characters; use a shorter name")
    if excerpt_lines is not None:
        if excerpt_lines < 1 or excerpt_lines > max_rows:
            raise ValueError(f"--excerpt-lines must be between 1 and {max_rows}")
        shown = rows[:excerpt_lines]
        if len(shown) < len(rows):
            title = f"Excerpt: first {len(shown)} of {len(rows)} display lines"
    else:
        shown = rows
    if len(shown) > max_rows:
        raise ValueError(f"poster holds {max_rows} display lines; use --excerpt-lines to label an excerpt")
    if display_width(title) > columns:
        raise ValueError("poster title does not fit; increase --columns or shorten --title")
    parts, panel_width, panel_height = panel(shown, columns, theme, panel_x, panel_y, title)
    positioning_lines = wrap_words(positioning, 38)
    if len(positioning_lines) > 2 or any(len(line) > 38 for line in positioning_lines):
        raise ValueError("positioning exceeds two lines; shorten --positioning")
    head = [f'<rect width="{width}" height="{height}" fill="{colours["paper"]}"/>',
            f'<text x="80" y="150" font-family="{SANS}" font-weight="700" font-size="{min(84, 1000 // max(1, display_width(name)))}" fill="{colours["ink"]}">{escape(name)}</text>']
    y = 215
    for line in positioning_lines:
        head.append(f'<text x="80" y="{y}" font-family="{SANS}" font-size="28" fill="{colours["ink"]}">{escape(line)}</text>')
        y += 36
    body = "\n".join(head + parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label={quoteattr(name + ": " + positioning)}>\n'
            f'{body}\n</svg>\n')


def wrap_words(sentence: str, columns: int) -> list[str]:
    lines, current = [], ""
    for word in sentence.split():
        candidate = f"{current} {word}".strip()
        if len(candidate) > columns and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [""]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("transcript", help="transcript file, or - for standard input")
    parser.add_argument("-o", "--output", default="-", help="SVG file to write (default: standard output)")
    parser.add_argument("--columns", type=int, default=80, help="wrap width in characters (default 80)")
    parser.add_argument("--theme", choices=sorted(THEMES), default="dark")
    parser.add_argument("--title", default="", help="text in the panel's title bar")
    parser.add_argument("--fit-content", action="store_true", help="shrink a capture to its longest display row (minimum 20 columns)")
    parser.add_argument("--poster", action="store_true", help="render a 1280x640 social preview")
    parser.add_argument("--excerpt-lines", type=int, help="poster only: show a labeled excerpt of this many display lines")
    parser.add_argument("--name", default="", help="project name for --poster")
    parser.add_argument("--positioning", default="", help="one positioning sentence for --poster")
    args = parser.parse_args(argv)
    if args.columns < 20 or args.columns > 200:
        parser.error("--columns must be between 20 and 200")
    if args.poster and not (args.name.strip() and args.positioning.strip()):
        parser.error("--poster needs --name and --positioning")
    if args.excerpt_lines is not None and not args.poster:
        parser.error("--excerpt-lines requires --poster")
    if args.fit_content and args.poster:
        parser.error("--fit-content is for captures only")
    try:
        for value in (args.name, args.title, args.positioning):
            if any(unsupported_control(char) for char in value):
                raise ValueError("titles and positioning must not contain control characters")
        rows = read_transcript(args.transcript, args.columns)
        if args.fit_content:
            args.columns = max(20, display_width(args.title), max(display_width(text) + (2 if kind == 'command' else 0) for kind, text in rows))
            if args.columns > 200:
                raise ValueError('capture title exceeds maximum width')
        if args.poster:
            document = poster(rows, args.columns, args.theme, args.title, args.name.strip(), args.positioning.strip(), args.excerpt_lines)
        else:
            document = capture(rows, args.columns, args.theme, args.title)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    if args.output == "-":
        sys.stdout.write(document)
    else:
        with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(document)
    return 0


if __name__ == "__main__":
    sys.exit(main())
