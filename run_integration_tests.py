import unittest
import sys

# Import the test module
from tests.test_nostr_publisher import TestNostrPublisher

# Load the test suite
suite = unittest.TestLoader().loadTestsFromTestCase(TestNostrPublisher)

# Run the tests
unittest.TextTestRunner(verbosity=2, stream=sys.stderr).run(suite)