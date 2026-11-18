@echo off
rem Build AEGIS_Studio.exe (run in this folder). Installs pywebview + pyinstaller. If numpy+scipy are present the live engine is bundled; otherwise the app runs on the precomputed grid.
python -m pip install --user -q pywebview pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name AEGIS_Studio ^
  --add-data "index.html;." --add-data "studio.js;." --add-data "data.js;." --add-data "classic.html;." --add-data "vendor;vendor" --add-data "engine;engine" ^
  --hidden-import scipy.integrate --hidden-import scipy.interpolate --hidden-import scipy.optimize app.py
copy /Y dist\AEGIS_Studio.exe "%USERPROFILE%\Desktop\AEGIS_Studio.exe" || copy /Y dist\AEGIS_Studio.exe "%USERPROFILE%\Desktop\AEGIS_Studio_new.exe"
