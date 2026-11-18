from datetime import date

import httpx

from .models import Paper


class ADSClient:
    endpoint = "https://api.adsabs.harvard.edu/v1/search/query"

    def __init__(self, token: str, timeout: float = 30.0, ca_bundle: str | None = None):
        if not token:
            raise ValueError("An ADS API token is required")
        self._client = httpx.Client(
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            timeout=timeout,
            verify=ca_bundle or True,
        )

    def search(self, query: str, rows: int = 50) -> list[Paper]:
        response = self._client.get(
            self.endpoint,
            params={"q": query, "fl": "bibcode,title,abstract,author,pubdate,doi,keyword", "rows": rows, "sort": "date desc"},
        )
        response.raise_for_status()
        records = response.json().get("response", {}).get("docs", [])
        papers: list[Paper] = []
        for record in records:
            bibcode = str(record.get("bibcode", ""))
            pubdate = record.get("pubdate")
            published = self._parse_date(pubdate)
            papers.append(Paper(
                source="ads",
                external_id=bibcode,
                title=(record.get("title") or [""])[0],
                abstract=record.get("abstract") or "",
                authors=record.get("author") or [],
                published=published,
                url=f"https://ui.adsabs.harvard.edu/abs/{bibcode}" if bibcode else "",
                doi=(record.get("doi") or [None])[0],
                categories=record.get("keyword") or [],
            ))
        return papers

    @staticmethod
    def _parse_date(value: str | None) -> date | None:
        if not value:
            return None
        try:
            return date.fromisoformat(value[:10])
        except (ValueError, TypeError):
            parts = value.split("-")
            if len(parts) >= 2:
                try:
                    return date(int(parts[0]), int(parts[1]), 1)
                except ValueError:
                    return None
            return None
