from typing import Annotated, Optional
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api_client import ApiError, api_client
from app.templating import templates

router = APIRouter()


@router.get("/items", response_class=HTMLResponse)
def list_items_page(request: Request):
    items = api_client.list_items()
    return templates.TemplateResponse(request, "items/list.html", {"items": items})


@router.get("/items/new", response_class=HTMLResponse)
def new_item_page(request: Request):
    return templates.TemplateResponse(request, "items/form.html")


@router.post("/items")
def create_item_action(
    request: Request,
    titre: Annotated[str, Form()],
    tarif_jour: Annotated[float, Form()],
    description: Annotated[Optional[str], Form()] = None,
    disponible: Annotated[bool, Form()] = False,
):
    payload = {
        "titre": titre,
        "tarif_jour": tarif_jour,
        "description": description if description else None,
        "disponible": disponible,
    }
    try:
        new_item = api_client.create_item(payload)
    except ApiError as exc:
        if exc.status_code == 422:
            return templates.TemplateResponse(
                request,
                "items/form.html",
                {
                    "erreurs": exc.messages(),
                    "saisie": payload,
                },
                status_code=422,
            )
        raise exc

    return RedirectResponse(f"/items/{new_item['id']}", status_code=303)

@router.get("/items/{item_id}", response_class=HTMLResponse)
def item_detail_page(request: Request, item_id: int):
    item = api_client.get_item(item_id)
    reservations = api_client.list_item_reservations(item_id)
    return templates.TemplateResponse(
        request,
        "items/detail.html",
        {"item": item, "reservations": reservations},
    )