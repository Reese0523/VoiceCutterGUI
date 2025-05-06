@echo off
REM —— 1. 若无 venv，就建一个
if not exist venv python -m venv venv
call venv\Scripts\activate.bat

REM —— 2. 安装/升级 pip & Nuitka
python -m pip install --upgrade pip
python -m pip install nuitka moviepy whisper tqdm numpy imageio_ffmpeg

REM —— 3. 用 Nuitka 编译成 single-file EXE
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
echo Build finished! EXE is at:
echo    %~dp0voice_cutter_gui.exe
pause
