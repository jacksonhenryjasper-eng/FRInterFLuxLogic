from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.controllers.auth_controller import AuthController

router = APIRouter()
auth_controller = AuthController()

class ApiKeyRequest(BaseModel):
    user_id: str
    email: str

@router.post("/api-key")
async def generate_api_key(request: ApiKeyRequest):
    """Generate a new API key for a user"""
    return auth_controller.generate_api_key(request.user_id, request.email)

@router.get("/validate")
async def validate_api_key(x_api_key: str = Header(...)):
    """Validate an API key"""
    try:
        return auth_controller.validate_api_key(x_api_key)
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error