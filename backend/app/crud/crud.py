from typing import Optional

from sqlalchemy.orm import Session

from app.models import models
from app.schemas import schemas
from app.utils import keygen


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    key = keygen.create_random_key()
    while get_db_url_by_key(db, key):
        key = keygen.create_random_key()

    secret_key = f"{key}{keygen.create_random_key()}"
    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_db_url_by_key(db: Session, url_key: str) -> Optional[models.URL]:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


def get_db_url_by_secret_key(db: Session, secret_key: str) -> Optional[models.URL]:
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL):
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)


def deactivate_db_url_by_secret_key(
    db: Session, secret_key: str
) -> Optional[models.URL]:
    db_url = get_db_url_by_secret_key(db, secret_key)

    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)

    return db_url
