#!/usr/bin/env python3
"""Read-only repository presentation facts; never execute a project's scripts."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
LEAK_EXIT = 7
TIMEOUT = 60
MAX_REPORT = 20 * 1024 * 1024


def environment():
    env = dict(os.environ)
    for name in list(env):
        if name.startswith(('GIT_', 'GITLEAKS_')):
            del env[name]
    env.update(LC_ALL='C', GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
    return env


def run(command, cwd):
    with subprocess.Popen(command, cwd=cwd, env=environment(), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace',
                          start_new_session=True) as process:
        try:
            stdout, stderr = process.communicate(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            # The scanner may own a Git child. Terminate its whole private group.
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            raise
        return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def git(root, *args):
    result = run(['git', '-C', str(root), *args], root)
    if result.returncode:
        raise ValueError('Git inspection failed; inspect repository access locally.')
    return result.stdout.strip()


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError('non-JSON constant')


def read_report(path):
    if not path.is_file() or path.stat().st_size > MAX_REPORT:
        raise ValueError('missing or oversized report')
    rows = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_keys,
                      parse_constant=invalid_constant)
    if not isinstance(rows, list):
        raise ValueError('report must be an array')
    for row in rows:
        if (not isinstance(row, dict) or not isinstance(row.get('RuleID'), str)
                or not row['RuleID'] or not isinstance(row.get('File'), str)
                or not row['File'] or type(row.get('StartLine')) is not int
                or row['StartLine'] < 1):
            raise ValueError('invalid finding record')
    return len(rows)


def scan(root, scope, scanner):
    if scanner is None:
        return {'status': 'unavailable', 'detail': 'Gitleaks not found in PATH.'}
    try:
        with tempfile.TemporaryDirectory(prefix='repo-craft-scan-') as temporary:
            private = Path(temporary)
            report = private / 'report.json'
            command = [scanner, 'git' if scope == 'history' else 'dir',
                       '--no-banner', '--no-color', '--redact=100', '--log-level=info',
                       '--exit-code', str(LEAK_EXIT), '--report-format=json',
                       '--report-path', str(report), '--config', str(HERE / 'scan-default.toml'),
                       '--gitleaks-ignore-path', str(private), '--ignore-gitleaks-allow',
                       '--timeout=45']
            if scope == 'history':
                command.append('--log-opts=--all')
            command.append(str(root))
            result = run(command, private)
            # Never copy scanner stdout/stderr, paths or finding values into the report.
            if result.returncode not in (0, LEAK_EXIT):
                return {'status': 'error', 'detail': f'Gitleaks exit {result.returncode}; logs withheld.'}
            if re.search(r'\b(ERR|FATAL)\b|^Error:', result.stderr + result.stdout, re.M):
                return {'status': 'error', 'detail': 'Scanner logged an error; logs withheld.'}
            count = read_report(report)
            if (result.returncode == LEAK_EXIT) != (count > 0):
                return {'status': 'error', 'detail': 'Exit status and parsed finding count disagree.'}
            evidence = {'findings': count, 'exitCode': result.returncode}
            if scope == 'history':
                counts = re.findall(r'\b(\d+) commits? scanned\b', result.stderr + result.stdout)
                if not counts or int(counts[-1]) == 0:
                    return {'status': 'error', 'detail': 'No positive commit scan count; coverage unverified.'}
                evidence['commitsScanned'] = int(counts[-1])
            return {'status': 'findings' if count else 'clean', **evidence}
    except subprocess.TimeoutExpired:
        return {'status': 'error', 'detail': 'Scanner exceeded timeout; child terminated.'}
    except (OSError, ValueError):
        return {'status': 'error', 'detail': 'Report missing, unreadable, oversized or invalid JSON/finding shape.'}


def read_text(root, filename):
    path = root / filename
    if any((root / Path(*Path(filename).parts[:i])).is_symlink() for i in range(1, len(Path(filename).parts) + 1)) or not path.is_file():
        return ''
    if path.stat().st_size > 2 * 1024 * 1024:
        return ''
    return path.read_text(encoding='utf-8', errors='replace')


class ImageSources(HTMLParser):
    """Collect literal HTML image sources; never fetch or execute HTML."""
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'img' and values.get('src'):
            self.targets.append(values['src'])
        if tag in ('img', 'source') and values.get('srcset'):
            self.targets.extend(item.strip().split()[0] for item in values['srcset'].split(',') if item.strip())


def image_sources(text):
    pattern = r'!\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)'
    parser = ImageSources()
    parser.feed(text)
    return re.findall(pattern, text) + parser.targets


def presentation(root):
    root = root.resolve()
    facts = {}
    flags = []
    def flag(kind, reason):
        flags.append({'kind': kind, 'reason': reason})
    def present(name):
        path = root / name
        return path.is_file() and not any((root / Path(*Path(name).parts[:i])).is_symlink() for i in range(1, len(Path(name).parts) + 1))
    facts['licensePresent'] = any(present(n) for n in ('LICENSE', 'LICENSE.md', 'LICENSE.txt', 'COPYING', 'UNLICENSE'))
    if not facts['licensePresent']:
        flag('evidence', 'No recognized license filename. Clarify reuse rights if offering code for reuse.')
    candidates = [str(Path(folder) / n) for folder in ('.github', '.', 'docs')
                  for n in ('README.md', 'README.rst', 'README.txt', 'README')]
    name = next((n for n in candidates if present(n)), None)
    facts['readmePresent'] = name is not None
    facts['readmePath'] = name
    text = read_text(root, name) if name else ''
    if not name:
        flag('evidence', 'No recognized README in .github, root or docs. Other case/format variants may exist.')
    top = '\n'.join(text.splitlines()[:30])
    images = image_sources(text)
    top_images = image_sources(top)
    badges = sum(bool(re.search(r'shields\.io|badgen\.net|badge', image, re.I)) for image in top_images)
    facts.update(sourceWindowLines=30, sourceWindowImageSyntaxMatches=len(top_images), sourceWindowBadgeHeuristicMatches=badges,
                 renderedViewportChecked=False, imageDiscovery='Inline Markdown and literal HTML src/srcset heuristics; reference-style images and renderer behavior require inspection.',
                 statusHeuristic=bool(re.search(r'(?im)(\*\*Status:?\*\*|^Status:|^##? Status)', text)))
    missing = 0
    outside = 0
    for target in set(images):
        parsed = urlsplit(target.strip('<>'))
        if parsed.scheme or parsed.netloc:
            continue
        base = root if parsed.path.startswith('/') else (root / name).parent
        path = (base / unquote(parsed.path).lstrip('/')).resolve()
        if not path.is_relative_to(root):
            outside += 1
        elif not path.is_file():
            missing += 1
    facts.update(localImageTargetsMissing=missing, localImageTargetsOutsideRepository=outside)
    if missing or outside:
        flag('evidence', 'Some detected image sources lack a file inside the repository. Inspect their links.')
    if badges > 4:
        flag('taste', 'Consider reducing badges if they delay the first useful command. Count is a heuristic, not a quality score.')
    facts['verifyCandidates'] = []
    try:
        package = json.loads(read_text(root, 'package.json') or '{}')
        scripts = package.get('scripts', {}) if isinstance(package, dict) else {}
        if isinstance(scripts, dict):
            facts['verifyCandidates'] += ['package.json:' + key for key in ('verify', 'check', 'test', 'build') if isinstance(scripts.get(key), str)]
    except ValueError:
        flag('evidence', 'package.json could not be parsed; verify discovery is incomplete.')
    makefile = read_text(root, 'Makefile')
    facts['verifyCandidates'] += ['make ' + key for key in ('verify', 'check', 'test') if re.search(r'^' + key + r'\s*:', makefile, re.M)]
    if not facts['verifyCandidates']:
        flag('heuristic', 'No package script or Make target detected. Look for documented checks before adding one.')
    facts['verifyExecuted'] = False
    facts['gitignorePresent'] = present('.gitignore')
    facts['envExamplePresent'] = present('.env.example')
    facts['socialPreviewPresent'] = any(present(n) for n in (
        'design/social/social-preview.png', 'design/social/social-preview.svg', '.github/social-preview.png'))
    site_files = ('index.html', 'docs/index.html', 'docs/_config.yml', '_config.yml',
                  'mkdocs.yml', 'astro.config.mjs', 'docusaurus.config.js')
    facts['websiteCandidates'] = [n for n in site_files if present(n)]
    if (root / 'site').is_dir():
        facts['websiteCandidates'].append('site/')
    workflows = root / '.github/workflows'
    if workflows.is_dir() and not workflows.is_symlink():
        for path in sorted(workflows.iterdir()):
            if path.suffix in ('.yml', '.yaml') and re.search('deploy-pages|upload-pages-artifact', read_text(root, str(path.relative_to(root)))):
                facts['websiteCandidates'].append('Pages workflow detected')
                break
    return facts, flags


def probe(directory):
    root = directory.resolve()
    if not root.is_dir():
        raise ValueError('Expected an existing readable directory.')
    git_state = 'not a repository'
    history = {'status': 'skipped', 'detail': 'No Git repository.'}
    commits = None
    tracked_env = None
    shallow = False
    if shutil.which('git'):
        result = run(['git', '-C', str(root), 'rev-parse', '--is-inside-work-tree'], root)
        if result.returncode == 0 and result.stdout.strip() == 'true':
            root = Path(git(root, 'rev-parse', '--show-toplevel')).resolve()
            git_dir = Path(git(root, 'rev-parse', '--absolute-git-dir')).resolve()
            common = Path(git(root, 'rev-parse', '--git-common-dir'))
            common = (root / common).resolve()
            git_state = 'linked worktree' if git_dir != common else 'repository'
            commits = int(git(root, 'rev-list', '--count', '--all'))
            shallow = git(root, 'rev-parse', '--is-shallow-repository') == 'true'
            tracked_env = sum(Path(p).name == '.env' for p in git(root, 'ls-files', '-z').split('\0') if p)
            history = scan(root, 'history', shutil.which('gitleaks')) if commits else {'status': 'skipped', 'detail': 'No commits on local refs.'}
        elif (root / '.git').exists():
            raise ValueError('Git metadata exists but Git cannot inspect it.')
    else:
        git_state = 'git unavailable'
        history = {'status': 'unavailable', 'detail': 'Git not found in PATH.'}
    working = scan(root, 'working-tree', shutil.which('gitleaks'))
    states = {history['status'], working['status']}
    overall = next(s for s in ('findings', 'error', 'unavailable', 'skipped', 'clean') if s in states)
    if shallow and overall == 'clean':
        overall = 'error'
    facts, flags = presentation(root)
    if tracked_env:
        flags.append({'kind': 'evidence', 'reason': 'Tracked .env file(s). Inspect contents; a filename alone does not prove a credential.'})
    return {'schemaVersion': 2, 'git': git_state, 'scope': 'repository root' if commits is not None else 'requested directory',
            'commitsOnLocalRefs': commits, 'shallow': shallow, 'trackedEnvFiles': tracked_env,
            'secretScan': {'status': overall, 'history': history, 'workingTree': working,
                           'policy': 'Installed Gitleaks built-in defaults; target config, ignore files and inline allow comments bypassed. No archive expansion; local refs only. Clean means no detections, not proof of no secrets.',
                           'coverageNote': 'Shallow history is incomplete.' if shallow else 'Unfetched remote refs, reflogs, submodule histories and external files are not covered.'},
            'presentation': facts, 'flags': flags}


def markdown(report):
    lines = ['# Repository presentation probe', '', '## Facts', '',
             '- git: ' + report['git'], '- scope: ' + report['scope'],
             '- commits on local refs: ' + str(report['commitsOnLocalRefs']),
             '- tracked .env files: ' + str(report['trackedEnvFiles']), '', '## Secret scan', '',
             '- secret-scan: ' + report['secretScan']['status']]
    for scope in ('history', 'workingTree'):
        value = report['secretScan'][scope]
        lines.append('- ' + scope + ': ' + json.dumps(value, sort_keys=True))
    lines += ['', report['secretScan']['policy'], report['secretScan']['coverageNote'],
              '', '## Presentation observations', '', '```json', json.dumps(report['presentation'], indent=2, sort_keys=True), '```',
              '', 'Verify candidates were discovered, not executed. Website candidates do not prove a Pages deployment.',
              '', '## Findings to interpret', '']
    lines += ['- ' + f['kind'].capitalize() + ': ' + f['reason'] for f in report['flags']]
    lines += ['', 'A missing visual is a design decision to consider, not a failed check. Review repository contents privately before sharing this report.']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', type=Path, default=Path.cwd())
    parser.add_argument('--json', action='store_true', help='emit structured facts instead of Markdown')
    args = parser.parse_args()
    try:
        result = probe(args.directory)
    except (ValueError, OSError, subprocess.TimeoutExpired):
        parser.exit(1, 'repo-probe: directory/Git inspection failed; check access and Git locally.\n')
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else markdown(result), end='\n' if args.json else '')


if __name__ == '__main__':
    main()
