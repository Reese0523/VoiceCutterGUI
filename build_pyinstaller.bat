@echo off
REM 调用系统 Python 解释器
set PYTHON=%PYTHON%  
IF NOT DEFINED PYTHON set PYTHON=python

"%PYTHON%" -m PyInstaller ^
  --clean ^
  --noconfirm ^
  --onefile ^
  --console ^
  --collect-submodules=moviepy ^
  --collect-submodules=whisper ^
  --collect-submodules=imageio_ffmpeg ^
  voice_cutter_gui.py

exit /b %errorlevel%
