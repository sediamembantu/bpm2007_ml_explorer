#!/bin/bash
# Run script for experiment tree using main's virtual environment
# Usage: ./run.sh [args]

MAIN_VENV="/data/Projects/bpm2007_ml_explorer/.venv/bin/python"

if [ ! -f "$MAIN_VENV" ]; then
    echo "Error: Main virtual environment not found at $MAIN_VENV"
    exit 1
fi

$MAIN_VENV main.py "$@"
