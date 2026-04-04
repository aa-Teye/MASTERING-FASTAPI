from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

# 1. Define where we expect to find the password (in the Request Header)
api_key_header = APIKeyHeader(name="X-Church-Key", auto_error=True)

# 2. Set the secure Admin Password (Later, we will hide this in a .env file)
ADMIN_SECRET_KEY = "onc-media-admin-2026"

def verify_admin(api_key: str = Security(api_key_header)):
    """
    Dependency function: Checks if the user provided the correct admin password.
    If they fail, it blocks them with a 401 Unauthorized error.
    """
    if api_key != ADMIN_SECRET_KEY;
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied: Invalid Church Admin Key",
        )
    return api_key