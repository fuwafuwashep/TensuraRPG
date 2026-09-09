"""Run Ren'Py lint/tests in a copy, isolating BOTH of Ren'Py's save locations.

Usage: python tools/run_checks.py C:/path/to/renpy-8.5.3-sdk [legacy-save-file]
Source/assets and compiled statement IDs are copied. The optional save fixture
is copied into the test sandbox; the game never writes to the original saves.
"""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(sys.argv[1]).resolve()
PROJECT = ROOT / '.checkpoints' / 'test-project'
REPORTS = ROOT / 'test-results'
PYTHON = SDK / 'lib' / 'py3-windows-x86_64' / 'python.exe'
REPORTS.mkdir(exist_ok=True)

def copy_changed(source, destination):
    source, destination = Path(source), Path(destination)
    if not destination.exists() or source.stat().st_mtime_ns != destination.stat().st_mtime_ns:
        shutil.copy2(source, destination)
    return str(destination)

shutil.copytree(ROOT / 'game', PROJECT / 'game', dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('saves', 'cache', '*.rpymc', '*.bak', '.vscode'),
                copy_function=copy_changed)

if len(sys.argv) > 2:
    legacy_file = Path(sys.argv[2]).resolve()
    (PROJECT / 'saves').mkdir(exist_ok=True)
    shutil.copy2(legacy_file, PROJECT / 'saves' / 'legacy-import-LT1.save')
    print('Testing legacy recovery using a copy of:', legacy_file.name)
else:
    # Ren'Py mirrors saves into game/saves, even with --savedir. Remove only our
    # previous fixture from both isolated locations so an omitted test stays off.
    for fixture in (PROJECT / 'saves' / 'legacy-import-LT1.save',
                    PROJECT / 'game' / 'saves' / 'legacy-import-LT1.save'):
        if not fixture.resolve().is_relative_to(PROJECT.resolve()):
            raise RuntimeError('Fixture path escaped the test project.')
        fixture.unlink(missing_ok=True)
    print('No legacy fixture supplied; legacy recovery case is inactive.')

for mode in ('lint', 'test'):
    command = [str(PYTHON), str(SDK / 'renpy.py'), str(PROJECT), mode]
    if mode == 'test':
        command += ['slice', '--overwrite-screenshots', '--report-detailed']
    command += ['--savedir', str(PROJECT / 'saves')]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=90)
    output = (result.stdout.decode('utf-8-sig', errors='replace') + result.stderr.decode('utf-8-sig', errors='replace')).replace('\r', '')
    (REPORTS / (mode + '.txt')).write_text(output, encoding='utf-8')
    print(output)
    if result.returncode:
        raise SystemExit(result.returncode)
    if mode == 'lint':
        warnings = output.split('Statistics:')[0].split('\n')[1:]
        if any(line.strip() for line in warnings):
            raise SystemExit('Lint reported warnings; inspect test-results/lint.txt')
    elif '[rpytest] Status: PASSED' not in output:
        raise SystemExit('Engine tests did not report success.')

screens = PROJECT / 'tests' / 'screenshots'
if screens.exists():
    shutil.copytree(screens, REPORTS / 'screenshots', dirs_exist_ok=True)
print('Lint and engine tests passed; reports and screenshots are in test-results/.')
