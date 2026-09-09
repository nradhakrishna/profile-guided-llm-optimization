def build_optimization_prompt(function, source):
    prompt = f"""
You are a Python performance optimization expert.

Analyze the following function and identify its main performance bottleneck. These are the stats that were taken from cprofiling.

Function: {function["name"]}
File: {function["file"]}
Execution time: {function["time"]:.6f} seconds
Call count: {function["calls"]}

Source code:
```python
{source}

Tasks:

Explain why this function is expensive.
Identify its algorithmic complexity.
Suggest an optimized implementation.
Explain why the proposed implementation should be faster.
Preserve the existing function interface and behavior.

IMPORTANT:
At the end of your response, provide the complete replacement implementation
of the function in exactly one Python code block.
The code block must contain the entire function, starting with def {function["name"]}.
Do not put any other Python code block after the replacement implementation.
"""
    return prompt