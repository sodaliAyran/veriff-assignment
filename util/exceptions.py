import logging
from typing import Callable

from fastapi import HTTPException


class DependencyException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DependencyTimeoutException(DependencyException):
    def __init__(self, func: Callable, dependency_name: str):
        logging.fatal(f"Call: '{func.__name__}' for '{dependency_name}' timed out.")
        super().__init__(status_code=500)


class DependencyUnknownException(DependencyException):
    def __init__(self, dependency_name: str, response_from_dependency: dict):
        logging.fatal(f"'{dependency_name}' call failed with unknown reasons: '{response_from_dependency}'")
        super().__init__(status_code=500)


class DependencyResponseValidationException(DependencyException):
    def __init__(self, func: Callable, dependency_name: str, e: Exception):
        logging.fatal(f"Failed to parse response from '{dependency_name}' for '{func.__name__}' call, '{e}'")
        super().__init__(status_code=500)


class DependencyEmptyResponseException(DependencyException):
    def __init__(self, func: Callable, dependency_name: str):
        logging.error(f"Response from '{dependency_name}' for '{func.__name__}' call, is empty.")
        super().__init__(status_code=400)


class DependencyBadRequestException(DependencyException):
    def __init__(self, dependency_name: str, response_from_dependency: dict):
        logging.fatal(f"Request to '{dependency_name}' is not valid '{response_from_dependency}'")
        super().__init__(status_code=400)
