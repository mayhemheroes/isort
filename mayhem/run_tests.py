#!/usr/bin/python3
"""run_tests.py — RUN isort's own pytest known-answer suite and print a parseable summary.

Invoked via the `/mayhem/isort-tests` ELF launcher (NOT directly), so the verify-repo
sabotage oracle can neuter the launcher and prove the test oracle is behavioral.

It runs a curated set of isort's real unit tests — thousands of parametrized known-answer
cases asserting isort.code(...) / isort.check_code(...) / api.sort_file(...) output EXACTLY —
writes a JUnit XML, parses the counts, and prints one line:

    RUNTESTS tests=<n> passed=<p> failed=<f> skipped=<s>

Exit 0 iff failed == 0. mayhem/test.sh parses that line into a CTRF report.

The selected files depend ONLY on isort + pytest (no black / hypothesis / libcst), so the
oracle runs without the heavy dev-tool dependency tree, yet still asserts isort's behavior
exhaustively: any no-op / "exit(0)" / behavior-altering patch to isort fails it.
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET

import pytest

XML = "/tmp/isort-junit.xml"
TESTS_DIR = "/mayhem/tests/unit"

# Known-answer suites that import only isort + pytest (no optional dev deps).
TEST_FILES = [
    f"{TESTS_DIR}/test_isort.py",
    f"{TESTS_DIR}/test_regressions.py",
    f"{TESTS_DIR}/test_ticketed_features.py",
    f"{TESTS_DIR}/test_api.py",
    f"{TESTS_DIR}/test_exceptions.py",
]


def main() -> int:
    pytest.main(["-q", "-p", "no:cacheprovider", *TEST_FILES, "--junitxml", XML])

    root = ET.parse(XML).getroot()
    suites = root.findall("testsuite") or ([root] if root.tag == "testsuite" else [])
    if not suites:
        print("RUNTESTS tests=0 passed=0 failed=1 skipped=0")
        return 1

    tests = failed = skipped = 0
    for s in suites:
        tests += int(s.get("tests", 0))
        failed += int(s.get("failures", 0)) + int(s.get("errors", 0))
        skipped += int(s.get("skipped", 0))
    passed = tests - failed - skipped

    print(f"RUNTESTS tests={tests} passed={passed} failed={failed} skipped={skipped}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
