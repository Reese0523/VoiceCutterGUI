@echo off
if not exist venv python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install nuitka moviepy whisper tqdm numpy imageio_ffmpeg

REM 关键改动：用 attach 而非 disable
python -m nuitka ^
  --standalone ^
  --onefile ^
  --windows-console-mode=attach ^
  --enable-plugin=tk-inter ^
  --assume-yes-for-downloads ^
  --include-package=moviepy ^
  --include-package=whisper ^
  --include-package=imageio_ffmpeg ^
  voice_cutter_gui.py

echo.
echo Build finished! EXE at:
echo    %~dp0voice_cutter_gui.exe
pause
