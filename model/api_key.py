from pydantic import BaseModel, UUID4


class ApiKey(BaseModel):
    key: UUID4
