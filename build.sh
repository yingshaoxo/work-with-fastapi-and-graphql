#!/bin/bash

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

pip install nuitka patchelf ordered-set zstandard
pip install --no-input -r requirements.txt

python3 -m nuitka --follow-imports --standalone --onefile  --remove-output --output-filename="program.run" main.py
echo -e "\nRun:\nprogram.run"
