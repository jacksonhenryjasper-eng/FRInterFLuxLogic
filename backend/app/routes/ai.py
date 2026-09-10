from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.routes.auth import auth_controller
from app.services.ai_provider import AIProviderError, generate_response

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


@router.post("/ask")
async def ask_ai(request: PromptRequest, x_api_key: str = Header(...)) -> dict:
    try:
        user = auth_controller.validate_api_key(x_api_key)
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error

    try:
        result = await generate_response(request.prompt, user["email"])
    except AIProviderError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    return {**result, "prompt": request.prompt}
