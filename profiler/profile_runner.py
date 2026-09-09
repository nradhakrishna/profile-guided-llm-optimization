import cProfile
from pathlib import Path

from benchmarks.benchmark import run_tests


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = PROJECT_ROOT / "benchmarks"


def profile_project():
    profiler = cProfile.Profile()

    profiler.enable()
    run_tests()
    profiler.disable()

    stats = profiler.getstats()

    project_functions = []

    for stat in stats:
        code = stat.code

        if not hasattr(code, "co_filename"):
            continue

        filename = Path(code.co_filename).resolve()

        if PROJECT_ROOT not in filename.parents:
            continue

        if BENCHMARK_DIR in filename.parents:
            continue

        project_functions.append({
            "name": code.co_name,
            "file": filename,
            "line": code.co_firstlineno,
            "calls": stat.callcount,
            "time": stat.totaltime
        })

    project_functions.sort(
        key=lambda function: function["time"],
        reverse=True
    )

    return project_functions