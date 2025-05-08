@echo off
REM 清理上次打包遺留
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist
if exist voice_cutter_gui.spec del /q voice_cutter_gui.spec
if exist voice_cutter_gui.log del /q voice_cutter_gui.log

REM 開始使用 PyInstaller 打包
"%PYTHON%"\python.exe -m PyInstaller ^
    --onefile ^
    --console ^
    --name voice_cutter_gui ^
    --log-level DEBUG ^
    --hidden-import moviepy.editor ^
    --hidden-import imageio_ffmpeg ^
    voice_cutter_gui.py

if errorlevel 1 (
    echo [ERROR] PyInstaller 打包失敗，請檢查輸出訊息。 >> voice_cutter_gui.log
    exit /b 1
)
