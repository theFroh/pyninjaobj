@echo off
cd /d "%~dp0"
python pyninjaobj.py --exists --tga %1
PAUSE
