# ========================================
# SCRIPT DE INICIO DEL BOT IA CLUB
# ========================================

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  INICIANDO BOT IA CLUB + CHATWOOT  " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# 1. Verificar entorno virtual
Write-Host "[1/4] Verificando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "$scriptDir\backend\venv\Scripts\python.exe") {
    Write-Host "   Entorno virtual encontrado" -ForegroundColor Green
    $pythonExe = "$scriptDir\backend\venv\Scripts\python.exe"
} else {
    Write-Host "   Usando Python del sistema" -ForegroundColor Yellow
    $pythonExe = "python"
}

# 2. Iniciar Backend
Write-Host "[2/4] Iniciando backend FastAPI..." -ForegroundColor Yellow
$backendCommand = "cd '$scriptDir\backend'; $pythonExe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand -PassThru -WindowStyle Normal
Write-Host "   Backend iniciado (PID: $($backendProcess.Id))" -ForegroundColor Green
Write-Host "   Esperando a que el servidor se inicie..." -ForegroundColor Gray
Start-Sleep -Seconds 8

# 2. Iniciar Backend
Write-Host "[2/4] Iniciando backend FastAPI..." -ForegroundColor Yellow
$backendCommand = "cd '$scriptDir\backend'; $pythonExe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand -PassThru -WindowStyle Normal
Write-Host "   Backend iniciado (PID: $($backendProcess.Id))" -ForegroundColor Green
Write-Host "   Esperando a que el servidor se inicie..." -ForegroundColor Gray
Start-Sleep -Seconds 8

# 3. Verificar que el backend esta corriendo
Write-Host "[3/4] Verificando backend..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/" -TimeoutSec 5
    Write-Host "   Backend OK: $($response.app) v$($response.version)" -ForegroundColor Green
} catch {
    Write-Host "   ERROR: Backend no responde" -ForegroundColor Red
    Write-Host "   Verifica la ventana de PowerShell del backend" -ForegroundColor Red
    exit 1
}

# 3. Verificar que el backend esta corriendo
Write-Host "[3/4] Verificando backend..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/" -TimeoutSec 5
    Write-Host "   Backend OK: $($response.app) v$($response.version)" -ForegroundColor Green
} catch {
    Write-Host "   ADVERTENCIA: Backend aun no responde (puede necesitar mas tiempo)" -ForegroundColor Yellow
    Write-Host "   Verifica la ventana de PowerShell del backend" -ForegroundColor Yellow
}

# 4. Iniciar ngrok
Write-Host "[4/4] Iniciando ngrok..." -ForegroundColor Yellow
$ngrokProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; .\ngrok.exe http 8000" -PassThru -WindowStyle Normal
Write-Host "   ngrok iniciado (PID: $($ngrokProcess.Id))" -ForegroundColor Green
Start-Sleep -Seconds 5

# 4. Obtener URL publica de ngrok
Write-Host ""
Write-Host "Obteniendo URL publica de ngrok..." -ForegroundColor Yellow
try {
    $tunnels = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -TimeoutSec 5
    $publicUrl = $tunnels.tunnels | Where-Object { $_.proto -eq 'https' } | Select-Object -First 1 -ExpandProperty public_url
    
    if ($publicUrl) {
        Write-Host ""
        Write-Host "=====================================" -ForegroundColor Green
        Write-Host "  SISTEMA INICIADO CORRECTAMENTE    " -ForegroundColor Green
        Write-Host "=====================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "URL PUBLICA DE NGROK:" -ForegroundColor Cyan
        Write-Host "$publicUrl" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "WEBHOOK PARA CHATWOOT:" -ForegroundColor Cyan
        Write-Host "$publicUrl/webhook/chatwoot" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "IMPORTANTE:" -ForegroundColor Red
        Write-Host "1. Copia la URL del webhook (arriba)" -ForegroundColor White
        Write-Host "2. Ve a Chatwoot -> Configuracion -> Integraciones -> Webhooks" -ForegroundColor White
        Write-Host "3. Edita el webhook y pega la nueva URL" -ForegroundColor White
        Write-Host "4. Asegurate de que este marcado: Mensaje creado" -ForegroundColor White
        Write-Host ""
        Write-Host "URLs DE ACCESO:" -ForegroundColor Cyan
        Write-Host "- Backend API: http://localhost:8000" -ForegroundColor White
        Write-Host "- Documentacion API: http://localhost:8000/docs" -ForegroundColor White
        Write-Host "- Panel ngrok: http://localhost:4040" -ForegroundColor White
        Write-Host "- Chatwoot: https://iaclub-chatwoot.ql7mr3.easypanel.host/app/accounts/2" -ForegroundColor White
        Write-Host ""
        Write-Host "Presiona Ctrl+C para cerrar esta ventana" -ForegroundColor Gray
        Write-Host "Las otras ventanas seguiran corriendo en segundo plano" -ForegroundColor Gray
        Write-Host ""
        
        # Copiar URL al clipboard
        Set-Clipboard -Value "$publicUrl/webhook/chatwoot"
        Write-Host "URL del webhook copiada al portapapeles" -ForegroundColor Green
        Write-Host ""
        
    } else {
        Write-Host "   ERROR: No se pudo obtener la URL de ngrok" -ForegroundColor Red
        Write-Host "   Verifica manualmente en: http://localhost:4040" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ERROR: ngrok no responde" -ForegroundColor Red
    Write-Host "   Verifica la ventana de PowerShell de ngrok" -ForegroundColor Red
    Write-Host "   O abre: http://localhost:4040" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
