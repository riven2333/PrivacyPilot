# pip install build twine
# Delete egg-info and dist directories
Get-ChildItem -Path . -Filter *.egg-info -Directory | Remove-Item -Recurse -Force
if (Test-Path dist) {
    Remove-Item -Path dist -Recurse -Force
}

# Rebuild the wheel
python -m build

# Check if the build was successful
if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful. Wheel file created in the dist directory." -ForegroundColor Green
    
    # List the contents of the dist directory
    Get-ChildItem -Path dist
} else {
    Write-Host "Build failed. Please check for errors." -ForegroundColor Red
}
twine upload dist/*
# pip install --index-url https://test.pypi.org/simple/ ppilot

# if everything ok
# twine upload dist/*