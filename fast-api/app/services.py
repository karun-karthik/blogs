from __future__ import annotations

from typing import Dict, List, Optional

import httpx

from .config import settings
from .models import Item
from .schemas import ExternalActivity, ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self) -> None:
        self._items: Dict[int, Item] = {
            1: Item(id=1, name="Notebook", description="A ruled notebook", price=9.99, tags=["stationery"]),
            2: Item(id=2, name="Pen", description="Smooth ink pen", price=2.5, tags=["stationery", "writing"]),
        }
        self._next_id = max(self._items.keys(), default=0) + 1

    def list_items(self, skip: int = 0, limit: int = 50, query: Optional[str] = None) -> List[Item]:
        items = list(self._items.values())
        if query:
            normalized = query.lower()
            items = [item for item in items if normalized in item.name.lower() or (item.description and normalized in item.description.lower())]
        return items[skip : skip + limit]

    def get_item(self, item_id: int) -> Optional[Item]:
        return self._items.get(item_id)

    def create_item(self, payload: ItemCreate) -> Item:
        item = Item(id=self._next_id, **payload.model_dump())
        self._items[self._next_id] = item
        self._next_id += 1
        return item

    def update_item(self, item_id: int, payload: ItemUpdate) -> Optional[Item]:
        existing = self._items.get(item_id)
        if existing is None:
            return None
        updated_data = payload.model_dump(exclude_unset=True)
        updated_item = existing.model_copy(update=updated_data)
        self._items[item_id] = updated_item
        return updated_item

    def delete_item(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None


async def fetch_external_activity(activity_type: Optional[str] = None, participants: Optional[int] = None) -> ExternalActivity:
    params: dict[str, str] = {}
    if activity_type:
        params["type"] = activity_type
    if participants is not None:
        params["participants"] = str(participants)

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(settings.external_activity_url, params=params)
        response.raise_for_status()
        payload = response.json()

    return ExternalActivity(**payload)
