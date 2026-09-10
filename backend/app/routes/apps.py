from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.app_discovery import app_registry

router = APIRouter()


class ConnectedApp(BaseModel):
    id: str
    name: str
    source: str
    status: str
    connectable: bool
    capabilities: List[str]


@router.get("", response_model=List[ConnectedApp])
async def list_apps() -> List[ConnectedApp]:
    return app_registry.list_apps()


@router.post("/scan", response_model=List[ConnectedApp])
async def scan_apps() -> List[ConnectedApp]:
    """Scan the local device for supported apps without opening them."""
    return app_registry.scan()
