from fastapi import APIRouter, Path, Query, HTTPException, Response  # type: ignore
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate  # type: ignore

router = APIRouter(prefix="/Items", tags=["Items"])

FAKE_DB: dict[int, dict] = {}
_next_id = 1

@router.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int = Path(ge=1)) -> ItemRead:
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} introuvable"
        )
    return item


@router.get("/items")
def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = None,
    disponible: bool | None = None,
):
    items = list(FAKE_DB.values())
    if q is not None:
        q_lower = q.lower()
        items = [item for item in items if q_lower in item["titre"].lower()]
    if disponible is not None:
        items = [item for item in items if item["disponible"] == disponible]
    return items[skip : skip + limit]


@router.post("/items", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate):
    global _next_id
    item = {"id": _next_id, **payload.model_dump()}
    FAKE_DB[_next_id] = item
    _next_id += 1
    return item

@router.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.update(payload.model_dump(exclude_unset=True))
    return item

@router.patch("/items/{item_id}", response_model=ItemRead)
def patch_item(item_id: int, payload: ItemUpdate):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item {item_id} not found")
    data = payload.model_dump(exclude_unset=True)
    item.update(data)
    return item

@router.delete("/items/{item_id}", status_code=204, response_class=Response)
def delete_item(item_id: int, int=Path(ge=1)):
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail="Item {item_id} not found")
    del FAKE_DB[item_id]
    