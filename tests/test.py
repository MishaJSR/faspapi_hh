from pydantic import BaseModel


class Some(BaseModel):
    some_int: int
    some_str: str

def get_some() -> list[Some]:
    return 4

print(get_some())