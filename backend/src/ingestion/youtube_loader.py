from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

from models.source_models import LoadedSourceContent


class YouTubeLoader:
    def __init__(self, source_id: str, title: str, url: str):
        self.source_id = source_id
        self.title = title
        self.url = url

    def _extract_video_id(self) -> str:
        parsed = urlparse(self.url)

        if parsed.hostname in ["www.youtube.com", "youtube.com"]:
            query = parse_qs(parsed.query)

            if "v" not in query:
                raise ValueError("Invalid YouTube URL: missing video id")

            return query["v"][0]

        if parsed.hostname == "youtu.be":
            return parsed.path.lstrip("/")

        raise ValueError("Invalid YouTube URL")

    def load(self) -> LoadedSourceContent:
        video_id = self._extract_video_id()

        try:
            api = YouTubeTranscriptApi()
            transcript = api.fetch(video_id, languages=["en"])

        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
            raise ValueError(f"Transcript unavailable for this video: {str(e)}")

        except Exception as e:
            raise ValueError(f"YouTube transcript extraction failed: {str(e)}")

        snippets = transcript.snippets

        text_parts = []
        segments = []

        for snippet in snippets:
            snippet_text = snippet.text.strip()

            if not snippet_text:
                continue

            start = float(snippet.start)
            duration = float(snippet.duration)

            text_parts.append(snippet_text)

            segments.append(
                {
                    "text": snippet_text,
                    "timestamp_start": round(start, 2),
                    "timestamp_end": round(start + duration, 2),
                }
            )

        combined_text = " ".join(text_parts).strip()

        if not combined_text:
            raise ValueError("Transcript was extracted but empty.")

        return LoadedSourceContent(
            user_id="temporary",
            source_id=self.source_id,
            source_type="youtube",
            title=self.title,
            text=combined_text,
            metadata={
                "video_id": video_id,
                "url": self.url,
                "segments": segments,
                "segment_count": len(segments),
            },
        )