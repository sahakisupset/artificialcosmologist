from pathlib import Path

from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection

from .models import Paper


class LiteratureIndex:
    def __init__(self, persist_directory: str = "./data/chroma", collection_name: str = "cosmology-literature"):
        resolved_directory = Path(persist_directory).expanduser().resolve()
        resolved_directory.mkdir(parents=True, exist_ok=True)
        self._client = PersistentClient(path=str(resolved_directory))
        self.collection: Collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def index(self, papers: list[Paper]) -> int:
        if not papers:
            return 0
        ids = [f"{paper.source}:{paper.external_id}" for paper in papers]
        documents = [paper.searchable_text for paper in papers]
        metadatas = [{
            "source": paper.source,
            "external_id": paper.external_id,
            "title": paper.title,
            "authors": ", ".join(paper.authors),
            "published": paper.published.isoformat() if paper.published else "",
            "url": paper.url,
            "doi": paper.doi or "",
            "categories": ", ".join(paper.categories),
        } for paper in papers]
        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        return len(papers)

    def search(self, query: str, limit: int = 10, where: dict | None = None) -> dict:
        return self.collection.query(
            query_texts=[query],
            n_results=limit,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

    @property
    def count(self) -> int:
        return self.collection.count()
