from typing import Annotated

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from requests import HTTPError

from app.api_client import ApiClient
from app.config import get_settings

app = FastAPI()


templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

api = ApiClient(get_settings().api_url)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("create_form.html", {"request": request})


@app.post("/create", response_class=HTMLResponse)
def create_response(request: Request, url: Annotated[str, Form()]):
    try:
        resp = api.create_url(url)
        return templates.TemplateResponse(
            "create_response.html", {"request": request, "response": resp}
        )
    except HTTPError as error:
        detail = error.response.json()["detail"]
        return templates.TemplateResponse(
            "error.html", {"request": request, "detail": detail}
        )


@app.get("/view", response_class=HTMLResponse)
def view_url_info_form(request: Request):
    return templates.TemplateResponse("view_form.html", {"request": request})


@app.post("/view", response_class=HTMLResponse)
def view_url_info_response(request: Request, secret_key: Annotated[str, Form()]):
    try:
        resp = api.get_url_admin_info(secret_key)
        return templates.TemplateResponse(
            "view_response.html", {"request": request, "response": resp}
        )
    except HTTPError as error:
        detail = error.response.json()["detail"]
        return templates.TemplateResponse(
            "error.html", {"request": request, "detail": detail}
        )


@app.get("/delete", response_class=HTMLResponse)
def delete_url_form(request: Request):
    return templates.TemplateResponse("delete_form.html", {"request": request})


@app.post("/delete", response_class=HTMLResponse)
def delete_url_response(request: Request, secret_key: Annotated[str, Form()]):
    try:
        resp = api.delete_url(secret_key)
        return templates.TemplateResponse(
            "delete_response.html", {"request": request, "message": resp}
        )
    except HTTPError as error:
        detail = error.response.json()["detail"]
        return templates.TemplateResponse(
            "error.html", {"request": request, "detail": detail}
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=get_settings().host, port=get_settings().port, reload=True
    )
