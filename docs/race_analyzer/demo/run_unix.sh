#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 -m venv .venv || python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -r requirements.txt
export DEMO_DATA_PATH="$(pwd)/demo_data.csv"
streamlit run app.py
