import time
from copy import deepcopy


def measure_runtime(function, test_input, runs=3):
    times = []

    for _ in range(runs):
        run_input = deepcopy(test_input)
        start = time.perf_counter()

        function(run_input)

        end = time.perf_counter()

        times.append(end - start)

    return min(times)


def compare_performance(
    original_function,
    optimized_function,
    test_input,
    runs=3
):
    original_time = measure_runtime(
        original_function,
        test_input,
        runs
    )

    optimized_time = measure_runtime(
        optimized_function,
        test_input,
        runs
    )

    speedup = original_time / optimized_time if optimized_time else float("inf")

    return {
        "original_time": original_time,
        "optimized_time": optimized_time,
        "speedup": speedup
    }
