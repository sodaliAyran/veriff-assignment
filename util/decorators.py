from fastapi import Response
from functools import wraps
from typing import Callable

from util.constants import MAX_UPLOAD_SIZE
from core import session_handler


def auth(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        api_key = request.headers.get("key")
        if api_key is None or not session_handler.authorize(api_key):
            return Response(status_code=403)
        return await func(*args, **kwargs)
    return wrapper


# This function is a pain to test therefore I'm skipping.
def image_size(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        file = kwargs.get("file")
        if not file.content_type.startswith('image'):
            return Response(status_code=400)

        if file.file.seekable():
            file.file.seek(0, 2)
            file_size = file.file.tell()
            file.file.seek(0)
            if file_size > MAX_UPLOAD_SIZE:
                return Response(status_code=413)
        return await func(*args, **kwargs)
    return wrapper



