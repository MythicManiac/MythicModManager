#!/bin/bash

pyinstaller --onefile manager/main.py
yes | cp -rf manager/config.json dist/config.json
yes | cp -rf package/icon.png dist/icon.png
yes | cp -rf package/manifest.json dist/manifest.json
yes | cp -rf package/README.md dist/README.md
mv -f dist/main.exe dist/MythicModManager.exe
