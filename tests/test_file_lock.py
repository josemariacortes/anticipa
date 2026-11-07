import subprocess
import sys
from pathlib import Path

from src.file_lock import acquire_nonblocking_lock


def test_lock_prevents_a_second_process_from_acquiring_it(tmp_path):
    lock_path = tmp_path / 'pilot.lock'
    script = (
        'import sys\n'
        'from pathlib import Path\n'
        'from src.file_lock import acquire_nonblocking_lock\n'
        'with Path(sys.argv[1]).open("a+b") as lock:\n'
        '    try:\n'
        '        acquire_nonblocking_lock(lock)\n'
        '    except BlockingIOError:\n'
        '        sys.exit(0)\n'
        'sys.exit(1)\n'
    )
    repository = Path(__file__).resolve().parents[1]

    with lock_path.open('a+b') as lock:
        acquire_nonblocking_lock(lock)
        blocked = subprocess.run(
            [sys.executable, '-c', script, str(lock_path)],
            cwd=repository,
            check=False,
        )
        assert blocked.returncode == 0

    released = subprocess.run(
        [sys.executable, '-c', script, str(lock_path)],
        cwd=repository,
        check=False,
    )
    assert released.returncode == 1
