from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from .schemas import ExternalActivity, ItemCreate, ItemResponse, ItemUpdate
from .services import ItemRepository, fetch_external_activity

router = APIRouter(prefix="", tags=["items"])
repository = ItemRepository()


@router.get("/", summary="API health check and metadata")
async def root() -> dict[str, str]:
    return {"message": "FastAPI CRUD Example is running", "version": "0.1.0"}


@router.get("/items", response_model=List[ItemResponse], summary="List all items")
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of items to return"),
    query: Optional[str] = Query(None, description="Optional search term for item name or description"),
) -> List[ItemResponse]:
    return repository.list_items(skip=skip, limit=limit, query=query)


@router.get("/items/{item_id}", response_model=ItemResponse, summary="Retrieve a single item")
async def get_item(item_id: int) -> ItemResponse:
    item = repository.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/items", response_model=ItemResponse, status_code=201, summary="Create a new item")
async def create_item(payload: ItemCreate) -> ItemResponse:
    return repository.create_item(payload)


@router.put("/items/{item_id}", response_model=ItemResponse, summary="Update an existing item")
async def update_item(item_id: int, payload: ItemUpdate) -> ItemResponse:
    updated = repository.update_item(item_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@router.delete("/items/{item_id}", status_code=204, summary="Delete an item")
async def delete_item(item_id: int) -> None:
    deleted = repository.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/external/activity", response_model=ExternalActivity, summary="Fetch an external activity")
async def external_activity(
    type: Optional[str] = Query(None, description="Filter the external activity by type"),
    participants: Optional[int] = Query(None, ge=1, le=10, description="Filter by number of participants"),
) -> ExternalActivity:
    return await fetch_external_activity(activity_type=type, participants=participants)
