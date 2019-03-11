#!/usr/bin/env bash

function reload() {
    pkill -f bot.py
    git pull
    sleep 5
    python3 bot.py
}

function setup() {
    python3 -m venv venv
    pip install -r requirements.txt
    python3 bot.py
}