import uvicorn
import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from app.config import get_settings
from app.crud import crud
from app.database import SessionLocal, engine
from app.models import models
from app.schemas import schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

BASE_URL = URL(f"http://{get_settings().host}:{get_settings().port}")


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


@app.get("/")
def docs_redirect():
    return RedirectResponse("/docs")


@app.post("/url", response_model=schemas.CreateURLResponse)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)
    response = db_url
    response.short_url = str(BASE_URL.replace(path=db_url.key))

    return response


@app.get("/{url_key}")
def redirect_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)

    raise HTTPException(status_code=404, detail=f"URL {request.url} doesn't exist")


@app.get(
    "/admin/{secret_key}",
    response_model=schemas.UrlAdminInfo,
)
def get_url_admin_info(secret_key: str, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        response = db_url
        response.short_url = str(BASE_URL.replace(path=db_url.key))
        return response

    raise HTTPException(status_code=404, detail="Invalid key")


@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, db: Session = Depends(get_db)):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}

    raise HTTPException(status_code=404, detail="Invalid key")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=get_settings().host, port=get_settings().port, reload=True
    )
