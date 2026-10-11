from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api_client import ApiError
from app.routers import items, reservations
from app.templating import BASE_DIR, templates

app = FastAPI(title="GearShare — Frontend")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(items.router)
app.include_router(reservations.router)


@app.get("/")
def home():
    return RedirectResponse(url="/items", status_code=303)


@app.exception_handler(ApiError)
def api_error_page(request: Request, exc: ApiError) -> HTMLResponse:
    messages = {
        404: "Cette ressource n'existe pas ou plus.",
        503: "Le service est momentanément indisponible. Réessayez dans un instant.",
    }
    msg = messages.get(exc.status_code, "Une erreur est survenue lors de la communication avec l'API.")
    return templates.TemplateResponse(
        request, "erreur.html", {"message": msg}, status_code=exc.status_code
    )