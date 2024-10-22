from typing import Optional

from pydantic import BaseModel, AnyUrl


class ConstructVacancy(BaseModel):
    url: AnyUrl
    name: str
    salary: str
    is_no_exp: bool
    is_remote: bool
    employer: str
    location: str
    is_active: Optional[bool] = True
