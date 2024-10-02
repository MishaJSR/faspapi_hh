from typing import Optional, Union

from pydantic import BaseModel


class ConstructUserId(BaseModel):
    user_id: int
