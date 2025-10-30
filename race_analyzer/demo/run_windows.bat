@echo off
cd /d "%~dp0"
if not exist .venv python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip >NUL
pip install -r requirements.txt
set DEMO_DATA_PATH=%CD%\demo_data.csv
streamlit run app.py
