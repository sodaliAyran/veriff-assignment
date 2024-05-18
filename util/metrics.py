import logging
import time
import functools


def latency(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        logging.info(f"Function '{func.__name__}' executed in {execution_time:.2f} ms")
        return result

    return wrapper
