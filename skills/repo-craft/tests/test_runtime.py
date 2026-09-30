"""Regression checks for host-path facts and truthful transcript rendering."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET


def module(name):
    path = Path(__file__).resolve().parents[1] / 'scripts' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


probe = module('repo_probe')
svg = module('terminal_to_svg')


class Presentation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def put(self, name, value=''):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)

    def test_host_precedence_and_relative_html_assets(self):
        self.put('README.md', '![Missing](no.png)')
        self.put('.github/README.md', '<picture><source srcset="../docs/dark.svg"><img src="../docs/light.svg"></picture>')
        self.put('docs/light.svg')
        self.put('docs/dark.svg')
        facts, _ = probe.presentation(self.root)
        self.assertEqual(facts['readmePath'], '.github/README.md')
        self.assertEqual(facts['localImageTargetsMissing'], 0)
        self.assertEqual(facts['sourceWindowImageSyntaxMatches'], 2)
        self.assertFalse(facts['renderedViewportChecked'])

    def test_root_relative_and_remote_sources(self):
        self.put('docs/README.md', '<img src="/assets/a.svg"><img src="https://example.com/a.png">')
        self.put('assets/a.svg')
        self.assertEqual(probe.presentation(self.root)[0]['localImageTargetsMissing'], 0)

    def test_missing_and_escape_counted_once(self):
        self.put('README.md', '![A](missing.png)\n![A](missing.png)\n<img src="../outside.png">')
        facts, _ = probe.presentation(self.root)
        self.assertEqual(facts['localImageTargetsMissing'], 1)
        self.assertEqual(facts['localImageTargetsOutsideRepository'], 1)

    def test_symlinked_parent_not_read(self):
        with tempfile.TemporaryDirectory() as other:
            (Path(other) / 'README.md').write_text('private content')
            (self.root / '.github').symlink_to(other, target_is_directory=True)
            self.put('README.md', '# Safe')
            self.assertEqual(probe.read_text(self.root, '.github/README.md'), '')
            self.assertEqual(probe.presentation(self.root)[0]['readmePath'], 'README.md')

    def test_source_window_not_visual_fold(self):
        self.put('README.md', '\n' * 31 + '![Later](a.svg)')
        self.assertEqual(probe.presentation(self.root)[0]['sourceWindowImageSyntaxMatches'], 0)


class Transcript(unittest.TestCase):
    def test_wide_combining_wrap_preserves_content(self):
        source = '測試e\u0301 & <result>'
        parts = svg.wrap(source, 5)
        self.assertEqual(''.join(parts), source)
        self.assertTrue(all(svg.display_width(part) <= 5 for part in parts))

    def test_plain_text_control_rejection(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / 'input.txt'
            for char in ('\x1b', '\x7f', '\u202e'):
                p.write_text('safe' + char + 'unsafe')
                with self.assertRaises(ValueError):
                    svg.read_transcript(str(p), 20)

    def test_xml_escaped_deterministic_and_no_external_refs(self):
        rows = [('command', 'echo <x> & y'), ('output', '測試')]
        a = svg.capture(rows, 30, 'dark', 'Actual <result>')
        self.assertEqual(a, svg.capture(rows, 30, 'dark', 'Actual <result>'))
        document = ET.fromstring(a)
        self.assertIn('echo <x> & y', ''.join(document.itertext()))
        self.assertNotIn('<circle', a)
        self.assertNotIn('href=', a)

    def test_poster_overflow_requires_explicit_excerpt(self):
        rows = [('output', str(i)) for i in range(25)]
        with self.assertRaises(ValueError):
            svg.poster(rows, 70, 'light', 'Result', 'Demo', 'Actual result')
        a = svg.poster(rows, 70, 'light', 'Result', 'Demo', 'Actual result', 3)
        self.assertIn('Excerpt: first 3 of 25', a)
        self.assertNotIn('>24</text>', a)

    def test_fit_content_cli_and_full_transcript(self):
        with tempfile.TemporaryDirectory() as folder:
            p, out = Path(folder) / 'input.txt', Path(folder) / 'out.svg'
            p.write_text('$ echo hello\nhello\n')
            self.assertEqual(svg.main([str(p), '--fit-content', '-o', str(out)]), 0)
            document = ET.parse(out).getroot()
            self.assertEqual(document.attrib['width'], str(int(20 * svg.CHAR_WIDTH + 2 * svg.PADDING)))
            self.assertEqual(''.join(document.itertext()).count('hello'), 2)


if __name__ == '__main__':
    unittest.main()
