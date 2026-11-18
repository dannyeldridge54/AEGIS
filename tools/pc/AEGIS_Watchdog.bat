@echo off
REM AEGIS watchdog: starts the PC runner, the CubeMind grading loop, the always-on learn loop and Ollama if any is not running.
REM Safe to run any time; it never stops or restarts something already running. Installed to run every 10 minutes and at sign-in.
set D=%USERPROFILE%\Desktop
set LOG=%D%\AEGIS_PCJOBS\queue\logs\watchdog.log
powershell -NoProfile -Command "if (Get-Process ollama -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" || ( start "" /min ollama serve & echo %date% %time% started ollama>>"%LOG%" )
wsl -e bash -c "pgrep -f 'pc_runne[r]' >/dev/null" || ( start "AEGIS PC runner" /min cmd /c "%D%\AEGIS_PC_RUNNER.bat" & echo %date% %time% started PC runner>>"%LOG%" )
powershell -NoProfile -Command "if (Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*evalsuite.gradeloo[p]*' }) { exit 0 } else { exit 1 }" || ( start "CubeMind grading loop" /min cmd /c "%D%\CubeMind_Grade_Loop.bat" & echo %date% %time% started grading loop>>"%LOG%" )
REM always-on self-learning loop (own process, NOT a batch job, so queue jobs can't starve it) — restart if it died
powershell -NoProfile -Command "if (Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*mindmem.learn_loo[p]*' }) { exit 0 } else { exit 1 }" || ( start "CubeMind learn loop" /min cmd /c "cd /d %USERPROFILE%\CubeMind_janus && python -m mindmem.learn_loop" & echo %date% %time% started learn loop>>"%LOG%" )
REM reaper: reclaim running/ slots left by crashed/hung/deadlocked jobs so the queue can never freeze (2026-11-18)
wsl -e bash /mnt/c/Users/Danny/Desktop/AEGIS_PCJOBS/reaper.sh >>"%LOG%" 2>&1
echo %date% %time% check done>>"%LOG%"
