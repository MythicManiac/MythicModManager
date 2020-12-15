#!/bin/bash

pyinstaller --onefile --noconsole main.py
yes | cp -rf package/icon.png dist/icon.png
yes | cp -rf package/manifest.json dist/manifest.json
yes | cp -rf package/README.md dist/README.md
mkdir -p dist/resources
yes | cp -rf resources/icon-unknown.png dist/resources/icon-unknown.png
mv -f dist/main.exe dist/MythicModManager.exe
