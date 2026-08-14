import os
from fastapi import Security, Depends, HTTPException, status, File, UploadFile
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from fastapi.security import APIKeyHeader
from app.core.logging import get_logger
from app.services.document import process_document

logger = get_logger(__name__)
router = APIRouter(prefix="/doctoapi", tags=["Document to Knowledge API"])

API_KEY = os.getenv("API_KEY", "tu-api-key-secreta")
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key():
    """
    Retrieve the API key from environment variables.
    Raises an exception if the API key is not set.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("API_KEY environment variable is not set.")
        raise RuntimeError("API_KEY environment variable is not set.")
    return api_key

def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if not api_key:
        logger.warning("Missing API Key in request headers.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: API Key required"
        )
    valid_key = get_api_key()
    if api_key != valid_key:
        logger.warning("Invalid API Key provided", extra={"provided_key": api_key})
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid API Key"
        )
    logger.info("API Key verified successfully")
    return api_key

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    logger.info("Health check requested")
    return {"status": "ok", "message": "API is running"}

@router.post("/document")
async def document(document: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    """
    Endpoint to process a document and convert it to knowledge.
    Requires a valid API key for access.
    """
    logger.info("Processing document", extra={"document": document})
    process_document(document.file.read())
    return {"status": "success", "message": "Document processed successfully", "document_id": str(uuid4())}