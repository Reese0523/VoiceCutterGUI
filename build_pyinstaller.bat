@echo off
REM ——— 清理旧文件 ———
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist
if exist voice_cutter_gui.spec del /q voice_cutter_gui.spec
if exist build.log         del /q build.log

REM ——— 打包并将日志重定向 ———
pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --console ^
  --name voice_cutter_gui ^
  wrapper.py ^
  > build.log 2>&1

IF ERRORLEVEL 1 (
  echo [ERROR] Packaging failed. See build.log below:
  type build.log
  exit /b 1
)

echo [OK] Packaging succeeded.
exit /b 0
