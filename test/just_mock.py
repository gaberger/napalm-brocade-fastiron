#!/usr/bin/env python

"""
Runs all mock tests.
"""

import unittest
from unit import test_fastiron

if __name__ == "__main__":
    # This creates a TextTestRunner (verbosity=2) and runs it with a test
    # suite composed by a list of desired test suites.
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([
        test_fastiron.MOCK_SUITE,
    ]))
