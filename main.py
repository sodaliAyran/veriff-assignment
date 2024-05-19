import logging
from typing import Optional

import uvicorn
from fastapi import FastAPI, Response, UploadFile, Header

from util.constants import Paths, MediaType
from model.summary import Summary
from util.decorators import auth, image_size
from model.api_key import ApiKey
from core import session_handler, summary_handler, encoder_handler
from util.exceptions import DependencyException

app = FastAPI()


@app.exception_handler(DependencyException)
def validation_exception_handler(request, exc):
    return Response(status_code=exc.status_code)


@app.get(Paths.PING.value, summary="A health check endpoint validate the service is up and running.")
async def ping():
    return Response(status_code=200)


@app.get(Paths.SESSION.value, response_model=ApiKey, summary="The endpoint to create user sessions.")
async def create_session():
    key = session_handler.create()
    return Response(content=ApiKey(key=key).json(),
                    media_type=MediaType.JSON.value,
                    status_code=200)


@app.delete(Paths.SESSION.value, summary="The endpoint to clear user sessions. "
                                         "You need to send your api key within the header.",
            status_code=204)
@auth
async def reset_session(key: Optional[str] = Header(None)):
    session_handler.reset(key)
    return Response(status_code=204)


@app.get(Paths.SUMMARY.value, response_model=Summary, summary="The endpoint for user to "
                                                              "get their face encoding summary.")
@auth
async def get_summary(key: Optional[str] = Header(None)):
    summary = summary_handler.get_summary(key)
    return Response(content=summary.json(),
                    media_type=MediaType.JSON.value,
                    status_code=200)


@app.post(Paths.ENCODE.value, summary="The endpoint for user to encode images.")
@auth
@image_size
async def upload_file(file: UploadFile, key: Optional[str] = Header(None)):
    file_content = await file.read()
    await encoder_handler.encode(key, file_content)
    return Response(status_code=200)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False, log_level=logging.INFO)
