from profiler.profile_runner import profile_project
from optimizer.source_extractor import get_function_source
from optimizer.prompt_builder import build_optimization_prompt
from optimizer.gemini_client import ask_gemini
from optimizer.code_extractor import extract_code
from optimizer.validator import load_function, validate_optimization
from optimizer.performance_validator import compare_performance
from functions.duplicates import find_duplicates


hotspots = profile_project()

top_function = hotspots[0]

source = get_function_source(top_function)

prompt = build_optimization_prompt(
    top_function,
    source
)

response = ask_gemini(prompt)

optimized_code = extract_code(
    response,
    top_function["name"]
)

print("\n=== EXTRACTED CODE ===\n")
print(optimized_code)


optimized_function = load_function(
    optimized_code,
    top_function["name"]
)


test_inputs = [
    [],
    [1],
    [1, 2, 3],
    [1, 2, 2, 3, 3],
    [1, 1, 1, 2, 2, 3],
    [5, 4, 3, 2, 1, 5, 4],
]


is_valid = validate_optimization(
    find_duplicates,
    optimized_function,
    test_inputs
)

print("\n=== VALIDATION ===")
print("PASS" if is_valid else "FAIL")


if is_valid:
    performance_input = [
        1, 2, 3, 4, 5,
        5, 6, 7, 8, 9,
        9, 10, 11, 12, 13
    ] * 1000

    results = compare_performance(
        find_duplicates,
        optimized_function,
        performance_input,
        runs=3
    )

    print("\n=== PERFORMANCE ===")
    print(
        f"Original time  : {results['original_time']:.6f} seconds"
    )
    print(
        f"Optimized time : {results['optimized_time']:.6f} seconds"
    )
    print(
        f"Speedup        : {results['speedup']:.2f}x"
    )