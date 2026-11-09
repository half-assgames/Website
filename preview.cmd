@echo off
rem Double-click to preview the website at http://localhost:8080/ . Close this window to stop.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0serve.ps1" -Open
