import importlib.util

from optimizer.code_extractor import extract_code
from optimizer.gemini_client import ask_gemini
from optimizer.performance_validator import compare_performance
from optimizer.prompt_builder import build_optimization_prompt
from optimizer.source_extractor import get_function_source
from optimizer.source_replacer import replace_function, restore_source
from optimizer.test_runner import run_tests
from optimizer.validator import load_function, validate_optimization
from profiler.profile_runner import PROJECT_ROOT, profile_project


TEST_INPUTS = {
    "find_duplicates": [
        [],
        [1],
        [1, 2, 3],
        [1, 2, 2, 3, 3],
        [1, 1, 1, 2, 2, 3],
        [5, 4, 3, 2, 1, 5, 4],
        [[1], [2], [1]],
    ],
    "create_sentence": [[], ["hello"], ["hello", "world"]],
    "find_common_items": [([], []), ([1, 2, 3], [2, 3, 4]), ([1, 1, 2], [1])],
}

PERFORMANCE_INPUTS = {
    "find_duplicates": [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13] * 1000,
    "create_sentence": ["hello"] * 100_000,
    "find_common_items": (list(range(10_000)), list(range(5_000, 15_000))),
}


def load_original_function(function):
    module_name = f"_optimization_target_{function['name']}"
    spec = importlib.util.spec_from_file_location(module_name, function["file"])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function["name"])


def adapt_cases(function):
    def wrapped(case):
        return function(*case) if isinstance(case, tuple) else function(case)
    return wrapped


def optimize(min_speedup=1.10):#check this out
    hotspots = profile_project()
    if not hotspots:
        raise RuntimeError("No project functions were captured by the profiler")

    target = hotspots[0]
    cases = TEST_INPUTS.get(target["name"])
    if cases is None:
        raise RuntimeError(f"No validation cases exist for {target['name']!r}")

    source = get_function_source(target)
    response = ask_gemini(build_optimization_prompt(target, source))
    optimized_code = extract_code(response, target["name"])
    if not optimized_code:
        raise RuntimeError("Gemini did not return an extractable replacement function")

    original = adapt_cases(load_original_function(target))
    optimized = adapt_cases(load_function(optimized_code, target["name"]))
    if not validate_optimization(original, optimized, cases):
        return {"status": "rejected", "reason": "validation failed"}

    results = compare_performance(
        original, optimized, PERFORMANCE_INPUTS[target["name"]], runs=5
    )
    if results["speedup"] < min_speedup:
        return {"status": "rejected", "reason": f"speedup {results['speedup']:.2f}x is below {min_speedup:.2f}x", **results}

    old_source = replace_function(target["file"], target["name"], optimized_code)
    try:
        test_result = run_tests(PROJECT_ROOT)
    except Exception:
        restore_source(target["file"], old_source)
        raise
    if test_result.returncode != 0:
        restore_source(target["file"], old_source)
        return {
            "status": "rolled_back",
            "reason": "full test suite failed after replacement",
            "test_output": test_result.stdout + test_result.stderr,
        }

    return {"status": "applied", "function": target["name"], "file": str(target["file"]), **results}


def main():
    print(optimize())


if __name__ == "__main__":
    main()
