@echo off

echo "Checking for Python"
where python >nul 2>&1
if %errorlevel%==0 (
    echo "Python is installed"
) else (
    echo "Python is not installed. Installing Python..."
    choco install python -y
)

echo "Checking for Pip"
where pip >nul 2>&1
if %errorlevel%==0 (
    echo "Pip is installed"
) else (
    echo "Pip is not installed. Installing Pip..."
    python -m ensurepip --upgrade
)

echo "Checking for SQLite3"
where sqlite3 >nul 2>&1
if %errorlevel%==0 (
    echo "SQLite3 is installed"
) else (
    echo "SQLite3 is not installed. Installing SQLite3..."
    choco install sqlite -y
)

echo "Unzipping Personal-Finance-Manager-Code.zip..."
powershell -Command "Expand-Archive -Path 'Personal-Finance-Manager-Code.zip' -DestinationPath 'Code' -Force"

echo "Running the main Python script"

python3 Code\main.py
