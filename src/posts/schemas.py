from typing import Optional

from pydantic import BaseModel


class ConstructVacancy(BaseModel):
    name: str
    url: str
    is_active: Optional[bool] = True
    registered_at: Optional[str] = None
