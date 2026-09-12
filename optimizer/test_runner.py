import subprocess
import sys


def run_tests(project_root, timeout=120):
    """Run unittest discovery in a fresh interpreter."""
    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
