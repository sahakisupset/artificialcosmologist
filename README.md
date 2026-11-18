# Cosmology Research Agent

A Phase 1 Python implementation for literature retrieval, knowledge indexing, reasoning, and assumption auditing.

## Features

- NASA ADS search client
- arXiv API ingestion
- ChromaDB persistent vector index
- DeepSeek-R1/OpenAI-compatible reasoning client
- Deterministic assumption auditor for age, boundary, expansion, symmetry, and origin assumptions

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Set `ADS_API_TOKEN` and `DEEPSEEK_API_KEY` in `.env` as needed.

## CLI

```powershell
cosmo-research ingest "cosmological redshift alternative" --arxiv --rows 25
cosmo-research ingest "tired light cosmology" --ads --rows 25
cosmo-research search "photon propagation vacuum structure"
cosmo-research audit docs/research_context.md
cosmo-research reason "Compare a propagation-based redshift model with Lambda-CDM without assuming metric expansion"
```

## Tests

```powershell
pytest
```
