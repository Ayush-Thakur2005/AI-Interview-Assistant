"""
MCP Tool: Code Execution
Runs candidate code against test cases in a sandboxed subprocess.
Supports Python, JavaScript (Node.js), and C++.
"""
import subprocess
import tempfile
import os
import time
import json
import resource
import logging
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

TIMEOUT = settings.SANDBOX_TIMEOUT

# MCP tool descriptor
CODE_RUNNER_TOOL_DESCRIPTOR = {
    "name": "run_code",
    "description": "Execute candidate code against test cases and return pass/fail results.",
    "input_schema": {
        "type": "object",
        "properties": {
            "language": {"type": "string", "enum": ["python", "javascript", "cpp"]},
            "code": {"type": "string"},
            "test_cases": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "input": {},
                        "expected": {},
                    },
                },
            },
        },
        "required": ["language", "code"],
    },
}


def run_code(
    language: str,
    code: str,
    test_cases: Optional[List[Dict[str, Any]]] = None,
) -> Dict:
    if not test_cases:
        test_cases = []

    results = []
    passed = 0
    total_runtime = 0.0

    for i, tc in enumerate(test_cases):
        result = _run_single_test(language, code, tc.get("input"), tc.get("expected"), i + 1)
        results.append(result)
        if result["passed"]:
            passed += 1
        if result.get("runtime_ms"):
            total_runtime += result["runtime_ms"]

    avg_runtime = total_runtime / len(test_cases) if test_cases else None

    return {
        "passed_tests": passed,
        "total_tests": len(test_cases),
        "runtime_ms": round(avg_runtime, 2) if avg_runtime else None,
        "memory_kb": None,  # OS-level measurement omitted for portability
        "results": results,
        "stdout": None,
        "error": None,
    }


def _run_single_test(language: str, code: str, input_data: Any, expected: Any, test_num: int) -> Dict:
    try:
        if language == "python":
            return _run_python(code, input_data, expected, test_num)
        elif language == "javascript":
            return _run_javascript(code, input_data, expected, test_num)
        elif language == "cpp":
            return _run_cpp(code, input_data, expected, test_num)
        else:
            return _error_result(test_num, input_data, expected, f"Unsupported language: {language}")
    except Exception as e:
        return _error_result(test_num, input_data, expected, str(e))


def _run_python(code: str, input_data: Any, expected: Any, test_num: int) -> Dict:
    """Wrap user code and call it with test input via subprocess."""
    harness = f"""
import json, sys

{code}

try:
    input_data = json.loads(sys.stdin.read())
    if isinstance(input_data, list):
        result = solution(*input_data)
    elif isinstance(input_data, dict):
        result = solution(**input_data)
    else:
        result = solution(input_data)
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({{"__error__": str(e)}}))
"""
    # Rename function to 'solution' for uniform calling
    normalised = _normalise_python_entry(code, harness)
    return _subprocess_run(
        ["python3", "-c", normalised],
        input_data=json.dumps(input_data),
        expected=expected,
        test_num=test_num,
    )


def _normalise_python_entry(code: str, harness: str) -> str:
    """Replace first def in user code with 'solution' alias appended."""
    import re
    match = re.search(r"^def (\w+)\s*\(", code, re.MULTILINE)
    if match:
        fn_name = match.group(1)
        alias = f"\nsolution = {fn_name}\n"
        return code + alias + "\n" + _harness_body()
    return harness


def _harness_body() -> str:
    return """
import json, sys
try:
    input_data = json.loads(sys.stdin.read())
    if isinstance(input_data, list):
        result = solution(*input_data)
    elif isinstance(input_data, dict):
        result = solution(**input_data)
    else:
        result = solution(input_data)
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"__error__": str(e)}))
"""


def _run_javascript(code: str, input_data: Any, expected: Any, test_num: int) -> Dict:
    import re
    match = re.search(r"function (\w+)\s*\(", code)
    fn_name = match.group(1) if match else "solution"
    harness = f"""
{code}

const fs = require('fs');
const inputData = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
try {{
    let result;
    if (Array.isArray(inputData)) {{
        result = {fn_name}(...inputData);
    }} else {{
        result = {fn_name}(inputData);
    }}
    console.log(JSON.stringify(result));
}} catch(e) {{
    console.log(JSON.stringify({{__error__: e.message}}));
}}
"""
    return _subprocess_run(
        ["node", "-e", harness],
        input_data=json.dumps(input_data),
        expected=expected,
        test_num=test_num,
    )


def _run_cpp(code: str, input_data: Any, expected: Any, test_num: int) -> Dict:
    """Compile and run C++ — requires g++ on the server."""
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "solution.cpp")
        exe = os.path.join(tmpdir, "solution")
        with open(src, "w") as f:
            f.write(code)
        compile_result = subprocess.run(
            ["g++", "-O2", "-o", exe, src],
            capture_output=True, text=True, timeout=15
        )
        if compile_result.returncode != 0:
            return _error_result(test_num, input_data, expected, f"Compile error: {compile_result.stderr}")
        return _subprocess_run(
            [exe],
            input_data=json.dumps(input_data),
            expected=expected,
            test_num=test_num,
        )


def _subprocess_run(cmd: List[str], input_data: str, expected: Any, test_num: int) -> Dict:
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        elapsed = (time.perf_counter() - start) * 1000

        stdout = proc.stdout.strip()
        if proc.returncode != 0 or not stdout:
            return _error_result(test_num, input_data, expected,
                                 proc.stderr.strip() or "Runtime error", elapsed)

        actual_raw = json.loads(stdout)
        if isinstance(actual_raw, dict) and "__error__" in actual_raw:
            return _error_result(test_num, input_data, expected, actual_raw["__error__"], elapsed)

        passed = actual_raw == expected
        return {
            "test_number": test_num,
            "passed": passed,
            "input": input_data,
            "expected": expected,
            "actual": actual_raw,
            "runtime_ms": round(elapsed, 2),
            "error": None,
        }
    except subprocess.TimeoutExpired:
        return _error_result(test_num, input_data, expected, f"Time limit exceeded ({TIMEOUT}s)")
    except Exception as e:
        return _error_result(test_num, input_data, expected, str(e))


def _error_result(test_num, input_data, expected, error, runtime_ms=None) -> Dict:
    return {
        "test_number": test_num,
        "passed": False,
        "input": input_data,
        "expected": expected,
        "actual": None,
        "runtime_ms": runtime_ms,
        "error": error,
    }
