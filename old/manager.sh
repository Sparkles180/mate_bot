#!/usr/bin/env bash

set -e

function reload() {
    git pull
    python3 bot.py
}

