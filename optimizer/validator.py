def load_function(source, function_name):
    namespace = {}

    exec(source, namespace)

    return namespace[function_name]


def validate_optimization(original_function, optimized_function, test_inputs):

    for test_input in test_inputs:
        original_result = original_function(test_input)
        try:
            optimized_result = optimized_function(test_input)
        except Exception:
            return False

        if original_result != optimized_result:
            return False

    return True
