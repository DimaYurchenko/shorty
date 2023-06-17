import requests
from pydantic import BaseModel, parse_obj_as


class URLBase(BaseModel):
    target_url: str


class URL(URLBase):
    is_active: bool
    clicks: int


class CreateURLResponse(BaseModel):
    short_url: str
    secret_key: str


class UrlAdminInfo(URL):
    short_url: str


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_url(self, target_url: str) -> CreateURLResponse:
        url = f"{self.base_url}/url"
        data = {"target_url": target_url}
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()
        return parse_obj_as(CreateURLResponse, response.json())

    def get_url_admin_info(self, secret_key: str) -> UrlAdminInfo:
        url = f"{self.base_url}/admin/{secret_key}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return parse_obj_as(UrlAdminInfo, response.json())

    def delete_url(self, secret_key: str) -> str:
        url = f"{self.base_url}/admin/{secret_key}"
        response = requests.delete(url, timeout=5)
        response.raise_for_status()
        return response.json()["detail"]
