from fastapi import HTTPException


def ensure_provider(payload):
    if payload is None:
        raise HTTPException(status_code=404, detail="provider_id not found")
    return payload

