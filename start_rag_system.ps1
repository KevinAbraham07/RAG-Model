# RAG System Startup Script
# This script starts the backend and opens the frontend

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  RAG System Startup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend is already running
$backendRunning = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($backendRunning) {
    Write-Host "✓ Backend already running on port 8000" -ForegroundColor Green
} else {
    Write-Host "Starting backend server..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; venv\Scripts\python.exe backend_api.py"
    Write-Host "✓ Backend starting on http://localhost:8000" -ForegroundColor Green
    Start-Sleep -Seconds 3
}

Write-Host ""
Write-Host "Opening frontend in browser..." -ForegroundColor Yellow
Start-Process "$PSScriptRoot\frontend.html"
Write-Host "✓ Frontend opened" -ForegroundColor Green

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  System Ready!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "Frontend: frontend.html (opened in browser)" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
