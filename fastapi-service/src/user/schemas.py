from typing import Optional, Union

from pydantic import BaseModel, conint


class ConstructUser(BaseModel):
    tg_user_id: int
    is_block_bot: Optional[bool] = False


class ResponseAllUsers(BaseModel):
    user_id: int
    tg_user_id: int
    is_block_bot: bool

