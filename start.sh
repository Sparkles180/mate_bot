#!/usr/bin/env bash

set -e

function setup() {
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 bot.py
}

function start() {
    while : ; do
        if [[ -d venv/ ]]; then
        source venv/bin/activate
        python3 bot.py
    else
        setup
     fi
     echo $?
    done

}

start