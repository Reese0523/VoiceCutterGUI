@echo off
REM 確保使用系統 python
set PY=python

echo 升級 pip 並安裝打包所需套件...
%PY% -m pip install --upgrade pip
%PY% -m pip install nuitka moviepy whisper tqdm numpy imageio_ffmpeg

echo 使用 Nuitka 進行打包...
%PY% -m nuitka --standalone --onefile --windows-console-mode=attach --enable-plugin=tk-inter --assume-yes-for-downloads --include-package=moviepy --include-package=whisper --include-package=imageio_ffmpeg voice_cutter_gui.py

if exist "%cd%\voice_cutter_gui.exe" (
  echo ==== Build succeeded: %cd%\voice_cutter_gui.exe ====
) else (
  echo ==== Build failed, please check above errors ====
)
pause
