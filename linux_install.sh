#!/bin/bash

echo "Checking for Python"
if command -v python3 >/dev/null 2>&1; then
    echo Python 3 is installed
else
    echo "Python is not installed. Installing Python..."
    sudo zypper install -y python3
fi

echo "Checking for Pip"
if command -v pip3 >/dev/null 2>&1; then
    echo "Pip is installed"
else
    echo "Pip is not installed. Installing Pip..."
    sudo zypper install -y python3-pip
fi

echo "Checking for SQLite3"
if command -v sqlite3 >/dev/null 2>&1; then
    echo "SQLite3 is installed"
else
    echo "SQLite3 is not installed. Installing SQLite3..."
    sudo zypper install -y sqlite3
fi

python3 Code/main.py
