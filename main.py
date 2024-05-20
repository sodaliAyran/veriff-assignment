import logging
from typing import Optional

import uvicorn
from fastapi import FastAPI, Response, UploadFile, Header

from config import MAX_UPLOAD_SIZE, SESSION_IMAGE_LIMIT
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


@app.get(Paths.PING.value,
         summary="A health check endpoint validate the service is up and running.",
         responses={200: {"description": "Service is healthy."}})
async def ping():
    return Response(status_code=200)


@app.get(Paths.SESSION.value,
         summary="The endpoint to create user sessions.",
         responses={200: {"description": "Session is created.",
                          "model": ApiKey}})
async def create_session():
    key = session_handler.create()
    return Response(content=ApiKey(key=key).json(),
                    media_type=MediaType.JSON.value,
                    status_code=200)


@app.delete(Paths.SESSION.value,
            summary="The endpoint to clear user sessions. You need to send your api key within the header.",
            responses={204: {"description": "Session images have been cleared."},
                       401: {"description": "API Key is missing or invalid."}
                       })
@auth
async def reset_session(key: Optional[str] = Header(None)):
    session_handler.reset(key)
    return Response(status_code=204)


@app.get(Paths.SUMMARY.value,
         summary="The endpoint for user to get their face encoding summary.",
         responses={200: {"description": "All the encodings belonging to the user.",
                          "model": Summary},
                    401: {"description": "API Key is missing or invalid."},
                    })
@auth
async def get_summary(key: Optional[str] = Header(None)):
    summary = summary_handler.get_summary(key)
    return Response(content=summary.json(),
                    media_type=MediaType.JSON.value,
                    status_code=200)


@app.post(Paths.ENCODE.value,
          summary="The endpoint for user to encode images.",
          responses={200: {"description": "Image has been encoded successfully."},
                     400: {"description": "There was a problem with the image. Possible issues:\n"
                                          "- File is not an image.\n"
                                          "- More than 5 faces are in the image.\n"
                                          "- There are no faces in the image."},
                     401: {"description": "API Key is missing or invalid."},
                     403: {"description": f"You have reached your encoding limit of {SESSION_IMAGE_LIMIT}"},
                     413: {"description": f"File size is bigger than {MAX_UPLOAD_SIZE} MB"},
                     500: {"description": "Internal server error. Contact API providers."}
                     })
@auth
@image_size
async def upload_file(file: UploadFile, key: Optional[str] = Header(None)):
    file_content = await file.read()
    encoder_handler.encode(key, file_content)
    return Response(status_code=200)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False, log_level=logging.INFO)
