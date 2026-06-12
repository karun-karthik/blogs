from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tags: List[str] = []
