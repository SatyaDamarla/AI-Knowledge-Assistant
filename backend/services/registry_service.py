import json
from pathlib import Path
from typing import List, Optional

from models.source_models import SourceRecord


class RegistryService:
    REGISTRY_PATH = Path("data/registry/sources.json")

    @classmethod
    def _ensure_registry_exists(cls) -> None:
        cls.REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

        if not cls.REGISTRY_PATH.exists():
            cls.REGISTRY_PATH.write_text("[]", encoding="utf-8")

    @classmethod
    def load_sources(cls) -> List[SourceRecord]:
        cls._ensure_registry_exists()

        raw_data = cls.REGISTRY_PATH.read_text(encoding="utf-8").strip()

        if not raw_data:
            return []

        data = json.loads(raw_data)
        return [SourceRecord(**item) for item in data]

    @classmethod
    def save_sources(cls, sources: List[SourceRecord]) -> None:
        cls._ensure_registry_exists()

        data = [source.model_dump() for source in sources]

        cls.REGISTRY_PATH.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def add_source(cls, source: SourceRecord) -> SourceRecord:
        sources = cls.load_sources()

        existing = cls.get_source(
            source_id=source.source_id,
            user_id=source.user_id,
        )

        if existing:
            raise ValueError(f"Source already exists: {source.source_id}")

        sources.append(source)
        cls.save_sources(sources)

        return source

    @classmethod
    def list_sources(cls, user_id: str) -> List[SourceRecord]:
        sources = cls.load_sources()

        return [
            source for source in sources
            if source.user_id == user_id
        ]

    @classmethod
    def get_source(
        cls,
        source_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[SourceRecord]:
        sources = cls.load_sources()

        for source in sources:
            if source.source_id != source_id:
                continue

            if user_id and source.user_id != user_id:
                continue

            return source

        return None

    @classmethod
    def update_source(
        cls,
        updated_source: SourceRecord,
        user_id: Optional[str] = None,
    ) -> SourceRecord:
        sources = cls.load_sources()

        for index, source in enumerate(sources):
            if source.source_id != updated_source.source_id:
                continue

            if user_id and source.user_id != user_id:
                continue

            sources[index] = updated_source
            cls.save_sources(sources)

            return updated_source

        raise ValueError(f"Source not found: {updated_source.source_id}")

    @classmethod
    def update_status(
        cls,
        source_id: str,
        status: str,
        user_id: Optional[str] = None,
    ) -> SourceRecord:
        source = cls.get_source(
            source_id=source_id,
            user_id=user_id,
        )

        if not source:
            raise ValueError(f"Source not found: {source_id}")

        source.status = status

        return cls.update_source(
            updated_source=source,
            user_id=user_id,
        )

    @classmethod
    def delete_source(
        cls,
        source_id: str,
        user_id: Optional[str] = None,
    ) -> bool:
        sources = cls.load_sources()

        remaining_sources = []

        deleted = False

        for source in sources:
            is_target = source.source_id == source_id
            belongs_to_user = user_id is None or source.user_id == user_id

            if is_target and belongs_to_user:
                deleted = True
                continue

            remaining_sources.append(source)

        if not deleted:
            return False

        cls.save_sources(remaining_sources)
        return True

    @classmethod
    def validate_source_ids(
        cls,
        source_ids: List[str],
        user_id: str,
    ) -> List[str]:
        allowed_sources = cls.list_sources(user_id=user_id)
        allowed_ids = {source.source_id for source in allowed_sources}

        return [
            source_id for source_id in source_ids
            if source_id in allowed_ids
        ]