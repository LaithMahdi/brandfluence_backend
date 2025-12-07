@echo off
REM Automatic Token Cleanup Script
REM This script runs the Django management command to delete expired tokens

cd /d %~dp0

REM Activate virtual environment (adjust path if needed)
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run the cleanup command
python manage.py cleanup_expired_tokens

REM Log the execution
echo [%date% %time%] Token cleanup executed >> logs\token_cleanup.log

REM Deactivate virtual environment
if exist venv\Scripts\deactivate.bat (
    call deactivate
)
