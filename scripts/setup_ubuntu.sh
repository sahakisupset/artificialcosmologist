#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential ca-certificates

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

if [[ ! -f .env ]]; then
    cp .env.example .env
    echo "Created .env. Add ADS_API_TOKEN and DEEPSEEK_API_KEY as needed."
fi

echo "Setup complete. Activate with: source .venv/bin/activate"
