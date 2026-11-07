@echo off
rem Double-click once. Starts the field tests now and schedules a nightly resume at 01:13 (finished runs are skipped,
rem so the nightly run only does what is left, then re-scores). Results go to the field-results branch.
rem Remove the schedule later with:  schtasks /Delete /TN "AEGIS field tests" /F
set "RUNNER=%~dp0RUN_FIELD_TESTS.bat"
schtasks /Create /TN "AEGIS field tests" /TR "\"%RUNNER%\" --push" /SC DAILY /ST 01:13 /F
start "AEGIS field tests" cmd /c ""%RUNNER%" --push"
echo Started now, and scheduled nightly at 01:13.
pause
