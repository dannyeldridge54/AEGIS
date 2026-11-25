@echo off
title AEGIS Field Engine
REM Usage: Field_Engine.bat [modelA] [modelB] [cycles]
set MA=%1
set MB=%2
set CY=%3
if "%MA%"=="" set MA=qwen3:14b
if "%MB%"=="" set MB=qwen3-coder:30b
if "%CY%"=="" set CY=40
cd /d "%USERPROFILE%\CubeMind_janus\field_engine"
python -m unittest test_engine || ( echo Engine self-test failed - not starting. & pause & exit /b 1 )
python engine.py --models %MA% %MB% --cycles %CY% --home field_engine_data
pause
