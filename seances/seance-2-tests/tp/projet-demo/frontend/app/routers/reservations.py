from datetime import date
from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from app.api_client import ApiError, api_client
from app.templating import templates

router = APIRouter()


@router.post("/items/{item_id}/reservations")
def create_reservation_action(
    request: Request,
    item_id: int,
    date_debut: Annotated[date, Form()],
    date_fin: Annotated[date, Form()],
):
    try:
        api_client.create_reservation(item_id, date_debut, date_fin)
    except ApiError as exc:
        if exc.status_code in (409, 422):
            item = api_client.get_item(item_id)
            reservations = api_client.list_item_reservations(item_id)
            return templates.TemplateResponse(
                request,
                "items/detail.html",
                {
                    "item": item,
                    "reservations": reservations,
                    "erreurs_reservation": exc.messages(),
                    "saisie": {"date_debut": date_debut, "date_fin": date_fin},
                },
                status_code=exc.status_code,
            )
        raise exc

    return RedirectResponse(f"/items/{item_id}?reservation=ok", status_code=303)


@router.post("/reservations/{reservation_id}")
def cancel_reservation_action(
    request: Request,
    reservation_id: int,
    item_id: Annotated[int, Form()],
):
    try:
        api_client.cancel_reservation(reservation_id)
    except ApiError as exc:
        if exc.status_code == 409:
            item = api_client.get_item(item_id)
            reservations = api_client.list_item_reservations(item_id)
            return templates.TemplateResponse(
                request,
                "items/detail.html",
                {
                    "item": item,
                    "reservations": reservations,
                    "erreur_globale": "Cette réservation est déjà annulée.",
                },
                status_code=409,
            )
        raise exc

    return RedirectResponse(f"/items/{item_id}?annulation=ok", status_code=303)