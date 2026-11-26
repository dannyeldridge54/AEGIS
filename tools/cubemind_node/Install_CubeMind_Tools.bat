@echo off
title Install CubeMind tools
echo Installing the CubeMind P1 tools (free, open source). This downloads from the internet.
python -m pip install --upgrade arxiv semanticscholar pyalex ollama sympy mpmath scipy pytest hypothesis sqlite-utils datasette networkx psutil nvidia-ml-py joblib
echo.
echo Pulling the embedding model for linking results by meaning...
ollama pull nomic-embed-text
echo.
echo Done. Close CubeMind Node 1 if it is running and start it again so it picks up the new tools.
pause
