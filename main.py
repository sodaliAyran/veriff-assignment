import logging

import uvicorn
from fastapi import FastAPI, Request, Response

from model.summary import Summary
from util.authorization import auth
from model.api_key import ApiKey
from core import session_handler, summary_handler

app = FastAPI()


@app.get("/ping")
async def ping():
    return Response(status_code=200)


@app.get("/session", response_model=ApiKey)
async def create_session():
    key = session_handler.create()
    return Response(content=ApiKey(key=key).json(), media_type="application/json", status_code=200)


@app.delete("/session")
@auth
async def reset_session(request: Request):
    session = request.headers.get("key")
    session_handler.reset(session)
    return Response(status_code=204)


@app.get("/summary", response_model=Summary)
@auth
async def get_summary(request: Request):
    session = request.headers.get("key")
    encoding = summary_handler.get_summary(session)
    return Response(content=encoding.json(), media_type="application/json", status_code=200)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=4000, reload=False, log_level=logging.INFO)
