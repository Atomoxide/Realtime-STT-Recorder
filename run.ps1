# Check if the virtual environment's Python executable exists
$venvPython = ".\.venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    # Run the Python script using the virtual environment's Python interpreter
    & $venvPython ".\recorder.py"
} else {
    Write-Host "Python executable not found in the virtual environment. Please ensure the virtual environment is correctly set up."
}
