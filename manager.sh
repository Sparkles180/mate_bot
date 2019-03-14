#!/usr/bin/env bash

set -e

function reload() {
    pkill -p bot.py
    git pull
    python3 bot.py
}

