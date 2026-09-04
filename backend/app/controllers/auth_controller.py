import secrets
from datetime import datetime
from typing import Dict, Optional

class AuthController:
    def __init__(self):
        # Simple in-memory storage for MVP (replace with database in production)
        self.api_keys: Dict[str, dict] = {}
    
    def generate_api_key(self, user_id: str, email: str) -> dict:
        """Generate a secure API key for a user"""
        # Generate a secure API key
        api_key = f"aib_{secrets.token_hex(32)}"
        
        # Store API key
        self.api_keys[api_key] = {
            "user_id": user_id,
            "email": email,
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
        
        return {
            "api_key": api_key,
            "message": "API key generated successfully. Keep this secure!"
        }
    
    def validate_api_key(self, api_key: str) -> dict:
        """Validate an API key and return user info"""
        key_data = self.api_keys.get(api_key)
        
        if not key_data or not key_data["is_active"]:
            raise ValueError("Invalid or inactive API key")
        
        return {
            "valid": True,
            "user_id": key_data["user_id"],
            "email": key_data["email"]
        }
    
    def get_user_from_api_key(self, api_key: str) -> Optional[dict]:
        """Get user info from API key"""
        key_data = self.api_keys.get(api_key)
        if key_data and key_data["is_active"]:
            return {
                "user_id": key_data["user_id"],
                "email": key_data["email"]
            }
        return None