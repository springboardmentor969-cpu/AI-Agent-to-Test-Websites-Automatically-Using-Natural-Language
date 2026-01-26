# Clear Python cache and restart Streamlit

Write-Host "=" -ForegroundColor Cyan
Write-Host "Clearing Python cache..." -ForegroundColor Yellow

# Remove __pycache__ directories
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Remove .pyc files
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "Cache cleared!" -ForegroundColor Green

Write-Host ""
Write-Host "Now please:" -ForegroundColor Cyan
Write-Host "1. Stop Streamlit (Ctrl+C in the terminal where it's running)" -ForegroundColor Yellow
Write-Host "2. Run: streamlit run ui/app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or just run this command:" -ForegroundColor Cyan
Write-Host "streamlit run ui/app.py" -ForegroundColor Green
