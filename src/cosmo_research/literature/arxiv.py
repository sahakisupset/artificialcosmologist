from datetime import date

import feedparser
import httpx

from .models import Paper


class ArxivIngestor:
    endpoint = "https://export.arxiv.org/api/query"

    def __init__(self, timeout: float = 30.0):
        self._timeout = timeout

    def search(self, query: str, max_results: int = 50) -> list[Paper]:
        response = httpx.get(
            self.endpoint,
            params={"search_query": f"all:{query}", "start": 0, "max_results": max_results, "sortBy": "submittedDate", "sortOrder": "descending"},
            timeout=self._timeout,
            headers={"User-Agent": "cosmo-research/0.1"},
        )
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        papers: list[Paper] = []
        for entry in feed.entries:
            external_id = entry.get("id", "").rstrip("/").rsplit("/", 1)[-1]
            published = self._parse_date(entry.get("published") or entry.get("updated") or "")
            doi = entry.get("arxiv_doi") or entry.get("doi")
            papers.append(Paper(
                source="arxiv",
                external_id=external_id,
                title=" ".join(entry.get("title", "").split()),
                abstract=" ".join(entry.get("summary", "").split()),
                authors=[author.name for author in entry.get("authors", [])],
                published=published,
                url=entry.get("link", ""),
                doi=doi,
                categories=[tag.term for tag in entry.get("tags", [])],
            ))
        return papers

    @staticmethod
    def _parse_date(value: str) -> date | None:
        try:
            from email.utils import parsedate_to_datetime
            parsed = parsedate_to_datetime(value)
            return parsed.date() if parsed else None
        except (TypeError, ValueError, OverflowError):
            return None
