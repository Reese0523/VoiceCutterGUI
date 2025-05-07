@echo off
set PY=python
%PY% -m pip install --upgrade pip
%PY% -m pip install pyinstaller moviepy whisper tqdm numpy imageio_ffmpeg

pyinstaller --clean --noupx --onedir --console voice_cutter_gui.spec
if exist dist\voice_cutter_gui.dist\voice_cutter_gui.exe (
    echo Build OK
) else (
    echo Build Failed, see log
)
pause
