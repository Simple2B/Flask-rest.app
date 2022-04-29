from pydantic import BaseModel


class ResponseMessage(BaseModel):
    description: str
    success: bool
