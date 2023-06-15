from pydantic import BaseModel


class URLBase(BaseModel):
    target_url: str


class URL(URLBase):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


class CreateURLResponse(BaseModel):
    short_url: str
    secret_key: str

    class Config:
        orm_mode = True


class UrlAdminInfo(URL):
    short_url: str
