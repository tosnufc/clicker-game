@echo off
title Scheduler - 24/7 Workflow Launcher
cd /d "%~dp0"

call .venv\Scripts\activate.bat
python scheduler_editor\scheduler_runner.py
