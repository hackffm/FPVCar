#!/bin/bash
if [ ! -d ~/fpvcar ]; then
  echo "create fpvcar folders"
  mkdir -p ~/fpvcar/logs
  mkdir -p ~/fpvcar/venv

  echo "create python3 venv"
  sudo apt-get install python3-venv
  python3 -m venv ~/fpvcar/venv
fi

echo "install requierements"
source ~/fpvcar/venv/bin/activate
pip install --upgrade pip
pip install -r requierements.txt