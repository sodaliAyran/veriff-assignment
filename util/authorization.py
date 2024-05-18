from fastapi import Response
from functools import wraps
from typing import Callable

from core import session_handler


def auth(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs["request"]
        api_key = request.headers.get("key")
        if api_key is None or not session_handler.authorize(api_key):
            return Response(status_code=403)
        return await func(*args, **kwargs)
    return wrapper




