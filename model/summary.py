from typing import List

from pydantic import BaseModel


class FaceEncoding(BaseModel):
    encoding: List[float]


class ImageEncoding(BaseModel):
    faces: List[FaceEncoding]


class Summary(BaseModel):
    image_encodings: List[ImageEncoding]
