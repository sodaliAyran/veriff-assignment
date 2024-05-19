import logging

import uvicorn
from fastapi import FastAPI, Request, Response, UploadFile

from constants import Paths, MediaType, API_KEY_REQUEST_HEADER_KEY
from model.summary import Summary
from util.decorators import auth, image_size
from model.api_key import ApiKey
from core import session_handler, summary_handler, encoder_handler

app = FastAPI()


@app.get(Paths.PING.value)
async def ping():
    return Response(status_code=200)


@app.get(Paths.SESSION.value, response_model=ApiKey)
async def create_session():
    key = session_handler.create()
    return Response(content=ApiKey(key=key).json(),
                    media_type=MediaType.JSON.value,
                    status_code=200)


@app.delete(Paths.SESSION.value)
@auth
async def reset_session(request: Request):
    session = request.headers.get(API_KEY_REQUEST_HEADER_KEY)
    session_handler.reset(session)
    return Response(status_code=204)


@app.get(Paths.SUMMARY.value, response_model=Summary)
@auth
async def get_summary(request: Request):
    session = request.headers.get(API_KEY_REQUEST_HEADER_KEY)
    summary = summary_handler.get_summary(session)
    return Response(content=summary.json(),
                    media_type=MediaType.JSON.value,
                    status_code=200)


@app.post(Paths.ENCODE.value)
#@auth
@image_size
async def upload_file(request: Request, file: UploadFile):
    file_content = await file.read()
    session = request.headers.get(API_KEY_REQUEST_HEADER_KEY)
    await encoder_handler.encode(session, file_content)
    return Response(status_code=200)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=4000, reload=False, log_level=logging.INFO)
