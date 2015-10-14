@echo off
cd /d "%~dp0"
python pyninjaobj.py %1 --exists --tga
PAUSE
