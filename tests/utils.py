import functools
import pytest

def assert_no_key_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyError:
            pytest.fail("Test raised KeyError")
    return wrapper