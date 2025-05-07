@echo off
set PY=python

echo Installing/upgrading pip and dependencies...
%PY% -m pip install --upgrade pip
%PY% -m pip install nuitka moviepy whisper tqdm numpy imageio_ffmpeg

echo Packaging with Nuitka (one-dir)...
%PY% -m nuitka --standalone --windows-console-mode=attach --enable-plugin=tk-inter --assume-yes-for-downloads --include-package=moviepy --include-package=whisper --include-package=imageio_ffmpeg voice_cutter_gui.py

if exist "%cd%\dist\voice_cutter_gui.dist\voice_cutter_gui.exe" (
    echo Build succeeded: dist\voice_cutter_gui.dist\voice_cutter_gui.exe
) else (
    echo Build failed, check console for errors.
)
pause
