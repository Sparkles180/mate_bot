#!/usr/bin/env bash

function reload() {
    git pull
    python3 bot.py
}

