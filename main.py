import subprocess
import sys


def main() -> int:
    """Run the Rahul Shetty Automation Practice Playwright test suite."""
    return subprocess.call([sys.executable, "-m", "pytest", "tests", "-v"])


if __name__ == "__main__":
    raise SystemExit(main())
