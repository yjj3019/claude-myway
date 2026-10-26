#!/usr/bin/env python3
"""tests/ 를 실행하고 실행 수를 확인한다. 테스트 0건이거나 skip이 있으면 실패로 본다."""
import sys
import unittest
from pathlib import Path


def run(start_dir):
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.discover(str(start_dir)))
    print(f"실행 {result.testsRun}건, 실패 {len(result.failures) + len(result.errors)}건, skip {len(result.skipped)}건")
    ok = result.wasSuccessful() and result.testsRun > 0 and not result.skipped
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run(Path(__file__).resolve().parent.parent / "tests"))
