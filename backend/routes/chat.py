from fastapi import APIRouter, Header
from models.api_models import QueryRequest, QueryResponse
from services.query_service import QueryService
from services.registry_service import RegistryService

router = APIRouter()
query_service = QueryService()


@router.post("/query", response_model=QueryResponse)
def query(
    request: QueryRequest,
    x_user_id: str = Header(...),
):
    safe_source_ids = RegistryService.validate_source_ids(
        source_ids=request.source_ids or [],
        user_id=x_user_id,
    )

    result = query_service.query(
        question=request.question,
        source_ids=safe_source_ids,
        user_id=x_user_id,
        top_k=request.top_k,
    )

    return QueryResponse(
        question=result["question"],
        answer=result["answer"],
        sources=result["sources"],
    )