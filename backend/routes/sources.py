import uuid

from fastapi import APIRouter, UploadFile, File, Header
from models.api_models import TextSourceRequest, YouTubeSourceRequest
from models.source_models import SourceRecord

from services.registry_service import RegistryService
from services.storage_service import StorageService

from src.ingestion.pipeline import IngestionPipeline


router = APIRouter()
pipeline = IngestionPipeline()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_user_id: str = Header(...),
):
    source_id, file_path = StorageService.save_uploaded_file(file)

    source = SourceRecord(
        user_id=x_user_id,
        source_id=source_id,
        source_type="pdf",
        title=file.filename,
        original_name=file.filename,
        storage_path=file_path,
        status="pending",
        metadata={"user_id": x_user_id},
    )

    RegistryService.add_source(source)
    pipeline.run(source)

    updated_source = RegistryService.update_status(
        source_id=source_id,
        status="indexed",
        user_id=x_user_id,
    )

    return updated_source


@router.get("")
def list_sources(x_user_id: str = Header(...)):
    return RegistryService.list_sources(user_id=x_user_id)


@router.get("/")
def list_sources_slash(x_user_id: str = Header(...)):
    return RegistryService.list_sources(user_id=x_user_id)


@router.post("/text")
def add_text_source(
    request: TextSourceRequest,
    x_user_id: str = Header(...),
):
    source_id = f"src_{uuid.uuid4().hex[:8]}"

    text_path = StorageService.save_text(
        source_id,
        request.text,
        source_type="text",
    )

    source = SourceRecord(
        user_id=x_user_id,
        source_id=source_id,
        source_type="text",
        title=request.title,
        raw_text_path=text_path,
        status="pending",
        metadata={"user_id": x_user_id},
    )

    RegistryService.add_source(source)
    pipeline.run(source)

    updated_source = RegistryService.update_status(
        source_id=source_id,
        status="indexed",
        user_id=x_user_id,
    )

    return updated_source


@router.post("/youtube")
def add_youtube_source(
    request: YouTubeSourceRequest,
    x_user_id: str = Header(...),
):
    source_id = f"src_{uuid.uuid4().hex[:8]}"

    source = SourceRecord(
        user_id=x_user_id,
        source_id=source_id,
        source_type="youtube",
        title=request.title,
        url=request.url,
        status="pending",
        metadata={"user_id": x_user_id},
    )

    RegistryService.add_source(source)
    pipeline.run(source)

    updated_source = RegistryService.update_status(
        source_id=source_id,
        status="indexed",
        user_id=x_user_id,
    )

    return updated_source