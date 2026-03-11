from pydantic import BaseModel

class APIKey(BaseModel):
    key: str
    description: str

class APIRequest(BaseModel):
    endpoint: str
    method: str
    payload: dict

class Configuration(BaseModel):
    timeout: int
    retries: int
