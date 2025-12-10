from typing import Callable, Dict, Any

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str):
        def decorator(func: Callable):
            self._tools[name] = func
            return func
        return decorator

    def get_tool(self, name: str) -> Callable:
        return self._tools.get(name)

    def list_tools(self):
        return list(self._tools.keys())

registry = ToolRegistry()

@registry.register("extract_functions")
def extract_functions_tool(code: str) -> list:
    """Extracts function definitions from the codebase."""
    return [line.strip() for line in code.splitlines() if line.strip().startswith("def ")]

@registry.register("check_complexity")
def check_complexity_tool(func_code: str) -> int:
    """Calculates cyclomatic complexity (simplified)."""
    return len(func_code)

@registry.register("lint_code")
def lint_code_tool(code: str) -> list:
    """Basic style checks."""
    issues = []
    if "print(" in code:
        issues.append("Avoid print statements, use logging.")
    if "TODO" in code:
        issues.append("Found TODO comment.")
    return issues
