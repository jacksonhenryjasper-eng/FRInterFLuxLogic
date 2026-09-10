from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Integration(BaseModel):
    id: str
    name: str
    description: str
    status: str


AVAILABLE_INTEGRATIONS: List[Integration] = [
    Integration(
        id="slack",
        name="Slack",
        description="Send AI-generated updates to a Slack workspace.",
        status="available",
    ),
    Integration(
        id="notion",
        name="Notion",
        description="Turn conversations into organized Notion pages.",
        status="available",
    ),
    Integration(
        id="github",
        name="GitHub",
        description="Use AI to summarize repositories and issues.",
        status="coming_soon",
    ),
]


@router.get("", response_model=List[Integration])
async def list_integrations() -> List[Integration]:
    return AVAILABLE_INTEGRATIONS
