@echo off
rmdir /s /q dist
rmdir /s /q build
del *.spec

pyinstaller ^
    --noconfirm ^
    --onefile ^
    --noconsole ^
    --add-data "assets/icon.ico:assets" ^
    --icon="assets/icon.ico" ^
    --name "BL4 Save Duplicator" ^
    src/main.py
