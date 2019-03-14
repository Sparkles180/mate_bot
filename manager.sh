#!/usr/bin/env bash

set -e

function reload() {
    pkill -f bot.py
    git pull
    python3 bot.py
}

