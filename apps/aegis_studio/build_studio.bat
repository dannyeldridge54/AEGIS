@echo off
rem Build AEGIS_Studio.exe (run in this folder). Installs pywebview + pyinstaller. If numpy+scipy are present the live engine is bundled; otherwise the app runs on the precomputed grid.
python -m pip install --user -q pywebview pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name Janus ^
  --add-data "index.html;." --add-data "studio.js;." --add-data "views3.js;." --add-data "strings3.js;." --add-data "dataplot.js;." --add-data "data.js;." --add-data "classic.html;." --add-data "vendor;vendor" --add-data "engine;engine" ^
  --hidden-import scipy.integrate --hidden-import scipy.interpolate --hidden-import scipy.optimize app.py
if not exist "%USERPROFILE%\Desktop\Janus_builds" mkdir "%USERPROFILE%\Desktop\Janus_builds"
copy /Y dist\Janus.exe "%USERPROFILE%\Desktop\Janus_builds\Janus.exe" || copy /Y dist\Janus.exe "%USERPROFILE%\Desktop\Janus_builds\Janus_new.exe"
