@echo off
REM AEGIS watchdog: starts the PC runner, grading loop, always-on learn loop and Ollama if any is not running.
REM Safe to run any time; never stops/restarts something already running EXCEPT a learn loop older than its own code (hot redeploy).
set D=%USERPROFILE%\Desktop
set LOG=%D%\AEGIS_PCJOBS\queue\logs\watchdog.log
powershell -NoProfile -Command "if (Get-Process ollama -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" || ( start "" /min ollama serve & echo %date% %time% started ollama>>"%LOG%" )
wsl -e bash -c "pgrep -f 'pc_runne[r]' >/dev/null" || ( start "AEGIS PC runner" /min cmd /c "%D%\AEGIS_PC_RUNNER.bat" & echo %date% %time% started PC runner>>"%LOG%" )
powershell -NoProfile -Command "if (Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*evalsuite.gradeloo[p]*' }) { exit 0 } else { exit 1 }" || ( start "CubeMind grading loop" /min cmd /c "%D%\CubeMind_Grade_Loop.bat" & echo %date% %time% started grading loop>>"%LOG%" )
REM hot redeploy: a learn loop started BEFORE its code was last edited is stale -> stop it (the next line relaunches it on the new code)
powershell -NoProfile -Command "$f=(Get-Item (Join-Path $env:USERPROFILE 'CubeMind_janus\mindmem\learn_loop.py')).LastWriteTime; Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*mindmem.learn_loo[p]*' -and $_.CreationDate -lt $f } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; Add-Content -Path (Join-Path $env:USERPROFILE 'Desktop\AEGIS_PCJOBS\queue\logs\watchdog.log') -Value ((Get-Date).ToString() + ' restarted learn loop (code updated)') }"
powershell -NoProfile -Command "if (Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*mindmem.learn_loo[p]*' }) { exit 0 } else { exit 1 }" || ( start "CubeMind learn loop" /min cmd /c "cd /d %USERPROFILE%\CubeMind_janus && python -m mindmem.learn_loop" & echo %date% %time% started learn loop>>"%LOG%" )
wsl -e bash /mnt/c/Users/Danny/Desktop/AEGIS_PCJOBS/reaper.sh >>"%LOG%" 2>&1
echo %date% %time% check done>>"%LOG%"
