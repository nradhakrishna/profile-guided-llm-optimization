import ast


def get_function_source(function):
    filename = function["file"]
    function_name = function["name"]

    with open(filename, "r") as f:
        source = f.read()

    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == function_name:
                lines = source.splitlines()

                start = node.lineno - 1
                end = node.end_lineno

                return "\n".join(lines[start:end])

    return None