from pydantic import BaseModel


class FastApiRabbit(BaseModel):
    tg_user_id : int

class FastApiRabbit2(BaseModel):
    tg_user_id : str