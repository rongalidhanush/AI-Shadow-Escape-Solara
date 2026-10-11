@echo off
cd /d "%~dp0"
python -m solara run solara_app.py --host 127.0.0.1 --port 8766
