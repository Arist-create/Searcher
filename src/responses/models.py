from typing import Any

from pydantic import BaseModel


class RespModelSearch(BaseModel):
    id: int
    text: str
    created_date: Any
    rubrics: list
