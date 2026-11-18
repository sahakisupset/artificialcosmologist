# Cosmology Research Agent

A Phase 1 Python implementation for literature retrieval, knowledge indexing, reasoning, and assumption auditing.

## Features

- NASA ADS search client
- arXiv API ingestion
- ChromaDB persistent vector index
- DeepSeek-R1/OpenAI-compatible reasoning client
- Deterministic assumption auditor for age, boundary, expansion, symmetry, and origin assumptions

## Setup

### Ubuntu

Install the system packages and project dependencies with:

```bash
bash scripts/setup_ubuntu.sh
source .venv/bin/activate
```

For a manual setup:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential ca-certificates
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp -n .env.example .env
```

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Set `ADS_API_TOKEN` and `DEEPSEEK_API_KEY` in `.env` as needed. On Ubuntu systems behind a corporate proxy, set `SSL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt` or point it to the proxy CA bundle.

## CLI

Activate the virtual environment and run the same commands on Ubuntu or Windows:

```bash
cosmo-research ingest "cosmological redshift alternative" --arxiv --rows 25
cosmo-research ingest "tired light cosmology" --ads --rows 25
cosmo-research search "photon propagation vacuum structure"
cosmo-research audit docs/research_context.md
cosmo-research reason "Compare a propagation-based redshift model with Lambda-CDM without assuming metric expansion"
```

## Tests

```bash
pytest
```
