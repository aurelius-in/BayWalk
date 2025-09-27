import os
from fastapi import Header, HTTPException
from typing import Optional


def require_api_key(x_api_key: Optional[str] = Header(default=None), authorization: Optional[str] = Header(default=None)) -> None:
    required = os.getenv("API_KEY", "").strip()
    if not required:
        return  # auth disabled

    provided = None
    if x_api_key:
        provided = x_api_key.strip()
    elif authorization and authorization.lower().startswith("bearer "):
        provided = authorization.split(" ", 1)[1].strip()

    if not provided or provided != required:
        raise HTTPException(status_code=401, detail="invalid or missing API key")
