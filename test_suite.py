"""
Compatibility test runner for the File System Recovery Tool.

Run this file directly to execute the unittest suite with verbose output.
"""

import unittest


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
