@echo off
title Browse CubeMind
cd /d "%~dp0"
echo Opening the CubeMind database in your browser (local only). Close this window to stop.
python -m datasette node1_data\node1.sqlite --open
