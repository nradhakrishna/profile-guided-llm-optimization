import re


def extract_code(response, function_name):
    pattern = rf"```python\s*(def\s+{re.escape(function_name)}\(.*?```)"
    
    match = re.search(
        pattern,
        response,
        re.DOTALL
    )

    if match:
        code = match.group(1)

        return code[:-3].strip()

    return None