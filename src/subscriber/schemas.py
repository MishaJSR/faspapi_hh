from pydantic import BaseModel, conint


class ConstructSubscriber(BaseModel):
    target: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: int
