from pydantic import BaseModel


class ConstructPost(BaseModel):
    name: str
    url: str
    is_active: bool
    registered_at: str
