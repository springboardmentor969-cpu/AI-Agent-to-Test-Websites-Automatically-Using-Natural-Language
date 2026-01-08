import subprocess
import sys


def run_generated_test(test_file_path: str) -> dict:
    cmd = [sys.executable, "-m", "pytest", test_file_path, "-q"]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    return {
        "status": "PASSED" if result.returncode == 0 else "FAILED",
        "exit_code": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }
