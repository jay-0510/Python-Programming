" UNIT TESTING - PYTHON "
# Its method of testing individual units or components of a software application to ensure they work as expected.
# A unit is the smallest testable part of any software. It usually has one or a few inputs and usually a single output.
# Python provides built-in and third-party frameworks, such as unittest (built-in) and pytest (third-party), for implementing unit tests.

" Core concepts of unit testing "
# Unit Test: Verifies a single unit of code (e.g., a function or method) in isolation.
# Test Case: A set of conditions or inputs used to test a specific function or component.
# Test Suite: A collection of test cases that can be run together.
# Assertions: Statements in test cases used to compare actual output with expected output.
# Setup and Teardown: Code to prepare the environment before a test (setup) and clean up after it (teardown).

" Unit Testing with unittest " # Built-in module
import unittest

# Code to test
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# Unit test class
class TestCalculator(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(2, 3), 5)  # Check if 2 + 3 = 5
        self.assertNotEqual(add(2, 3), 6)  # Check that 2 + 3 ≠ 6

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)  # Check if 10 - 5 = 5
        self.assertNotEqual(subtract(10, 5), 4)  # Check that 10 - 5 ≠ 4

if __name__ == "__main__":
    unittest.main()
    
    
" Assertions in unittest "
#     Assertion                              Description
# self.assertEqual(a, b)	           Verifies a == b.
# self.assertNotEqual(a, b)	           Verifies a != b.
# self.assertTrue(expr)	               Verifies expr is True.
# self.assertFalse(expr)	           Verifies expr is False.
# self.assertIs(a, b)	               Verifies a is b.
# self.assertIsNot(a, b)	           Verifies a is not b.
# self.assertIn(a, b)	               Verifies a in b.
# self.assertNotIn(a, b)	           Verifies a not in b.
# self.assertRaises(error)	       Checks if an exception is raised. 
 