@echo off
rmdir /s /q dist
rmdir /s /q build
del *.spec

pyinstaller ^
    --noconfirm ^
    --onefile ^
    --noconsole ^
    --add-data "assets/icon.ico:assets" ^
    --add-data "version.txt:." ^
    --icon="assets/icon.ico" ^
    --name "BL4_Save_Duplicator" ^
    src/main.py
