from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, constr, conlist, HttpUrl


class ItemCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: constr(min_length=1, strip_whitespace=True) = Field(
        ..., description="A descriptive name for the item"
    )
    description: Optional[constr(max_length=300, strip_whitespace=True)] = Field(
        None,
        description="An optional description for the item",
    )
    price: PositiveFloat = Field(..., description="The price must be greater than 0")
    tags: conlist(constr(min_length=1), unique_items=True) = Field(
        default_factory=list,
        description="A list of tags to categorize the item",
    )


class ItemUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[constr(min_length=1, strip_whitespace=True)] = Field(
        None, description="Updated name for the item"
    )
    description: Optional[constr(max_length=300, strip_whitespace=True)] = Field(
        None, description="Updated description for the item"
    )
    price: Optional[PositiveFloat] = Field(
        None, description="Updated price for the item"
    )
    tags: Optional[conlist(constr(min_length=1), unique_items=True)] = Field(
        None, description="Updated list of tags for the item"
    )


class ItemResponse(ItemCreate):
    id: int


class ExternalActivity(BaseModel):
    activity: str
    type: str
    participants: int
    price: float
    link: Optional[HttpUrl] = None
    key: str
    accessibility: float
