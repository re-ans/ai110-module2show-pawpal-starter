"""
Simple test runner for PawPal+ tests (alternative to pytest)
"""

import sys
import traceback
from tests.test_pawpal import TestTask, TestPet, TestOwner, TestScheduler, TestSchedulerAlgorithms


def run_test_class(test_class):
    """Run all test methods in a test class."""
    instance = test_class()
    test_methods = [method for method in dir(instance) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    print(f"\n{'=' * 60}")
    print(f"Running tests from {test_class.__name__}")
    print('=' * 60)
    
    for method_name in test_methods:
        try:
            method = getattr(instance, method_name)
            method()
            print(f"✓ {method_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {method_name}")
            print(f"  Error: {str(e)}")
            traceback.print_exc()
            failed += 1
    
    return passed, failed


def main():
    """Run all tests."""
    total_passed = 0
    total_failed = 0
    
    test_classes = [TestTask, TestPet, TestOwner, TestScheduler, TestSchedulerAlgorithms]
    
    for test_class in test_classes:
        passed, failed = run_test_class(test_class)
        total_passed += passed
        total_failed += failed
    
    print(f"\n{'=' * 60}")
    print(f"Test Results: {total_passed} passed, {total_failed} failed")
    print('=' * 60)
    
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
