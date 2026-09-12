import ast
import os
import tempfile
from pathlib import Path


def _validate_replacement(source, function_name):
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if len(functions) != 1 or functions[0].name != function_name:
        raise ValueError(f"Replacement must contain exactly one top-level function named {function_name!r}")
    return source.rstrip() + "\n"


def _atomic_write(path, content):
    mode = path.stat().st_mode
    descriptor, temporary_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w") as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def replace_function(filename, function_name, replacement_source):
    """Atomically replace one top-level function and return the old file text."""
    path = Path(filename)
    original = path.read_text()
    tree = ast.parse(original)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one top-level function named {function_name!r}")

    replacement = _validate_replacement(replacement_source, function_name)
    node = matches[0]
    start_line = min([node.lineno] + [item.lineno for item in node.decorator_list])
    lines = original.splitlines(keepends=True)
    updated = "".join(lines[:start_line - 1]) + replacement + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    _atomic_write(path, updated)
    return original


def restore_source(filename, original_source):
    _atomic_write(Path(filename), original_source)
