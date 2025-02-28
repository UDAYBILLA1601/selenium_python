"""
This module provides functions for raising assertions in test steps.
It includes both soft assertions (which allow test execution to continue)
and hard assertions (which halt execution on failure).
"""

from pytest_check import check

def soft_assert(condition: bool, msg: str) -> None:
    """
    Perform a soft assertion using pytest-check.

    Soft assertions allow test execution to continue even if the assertion fails.

    Args:
        condition (bool): A boolean condition to evaluate.
                         If True, the test step passes.
                         If False, an assertion failure is recorded, but execution continues.
        msg (str): The message displayed if the assertion fails.

    Returns:
        None
    """
    check.is_true(condition, msg)

def hard_assert(condition: bool, msg: str) -> None:
    """
    Perform a hard assertion.

    Hard assertions stop test execution immediately if the assertion fails.

    Args:
        condition (bool): A boolean condition to evaluate.
                         If True, the test step passes.
                         If False, an AssertionError is raised, stopping execution.
        msg (str): The message displayed if the assertion fails.

    Returns:
        None

    Raises:
        AssertionError: If the condition evaluates to False.
    """
    assert condition, msg
