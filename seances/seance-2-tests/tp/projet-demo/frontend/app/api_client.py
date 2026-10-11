import os
from datetime import date
from typing import Any, List

import httpx


class ApiError(Exception):
    """Erreur levée lors d'un échec de l'API REST."""

    def __init__(self, status_code: int, detail: Any) -> None:
        super().__init__(f"{status_code}: {detail}")
        self.status_code = status_code
        self.detail = detail

    def messages(self) -> List[str]:
        """Transforme le détail d'erreur en liste de messages lisibles."""
        if isinstance(self.detail, str):
            return [self.detail]
        if isinstance(self.detail, list):
            res = []
            for err in self.detail:
                if isinstance(err, dict):
                    loc = err.get("loc", [])
                    field = loc[-1] if loc else "Champ"
                    msg = err.get("msg", "Valeur invalide")
                    res.append(f"{field} : {msg}")
                else:
                    res.append(str(err))
            return res
        return ["Une erreur est survenue."]


class ApiClient:
    """Porte d'entrée unique du frontend vers l'API du backend."""

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self._http = httpx.Client(base_url=base_url, timeout=timeout)

    def _send(self, method: str, url: str, **kwargs: Any) -> Any:
        try:
            response = self._http.request(method, url, **kwargs)
        except httpx.RequestError as exc:
            raise ApiError(503, "Le service backend est indisponible.") from exc

        if response.is_error:
            try:
                detail = response.json().get("detail")
            except Exception:
                detail = response.text
            raise ApiError(response.status_code, detail)

        return response.json() if response.content else None

    def list_items(self) -> List[dict[str, Any]]:
        return self._send("GET", "/items")

    def get_item(self, item_id: int) -> dict[str, Any]:
        return self._send("GET", f"/items/{item_id}")

    def create_item(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._send("POST", "/items", json=data)

    def list_item_reservations(self, item_id: int) -> List[dict[str, Any]]:
        return self._send("GET", "/reservations", params={"item_id": item_id})

    def create_reservation(self, item_id: int, date_debut: date, date_fin: date) -> dict[str, Any]:
        return self._send(
            "POST",
            "/reservations",
            json={
                "item_id": item_id,
                "date_debut": date_debut.isoformat(),
                "date_fin": date_fin.isoformat(),
            },
        )

    def cancel_reservation(self, reservation_id: int) -> dict[str, Any]:
        return self._send("POST", f"/reservations/{reservation_id}/annuler")

api_client = ApiClient(base_url=os.getenv("API_BASE_URL", "http://backend:8000"))