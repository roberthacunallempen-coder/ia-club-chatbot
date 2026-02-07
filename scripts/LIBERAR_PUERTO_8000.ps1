# ========================================
# LIBERAR PUERTO 8000
# ========================================

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "    LIBERANDO PUERTO 8000" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Buscar proceso usando el puerto 8000
Write-Host "Buscando procesos en puerto 8000..." -ForegroundColor Yellow

$connections = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($connections) {
    Write-Host ""
    Write-Host "Procesos encontrados:" -ForegroundColor Green
    
    $processes = @()
    foreach ($conn in $connections) {
        $process = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            $processes += $process
            Write-Host "  - $($process.ProcessName) (PID: $($process.Id))" -ForegroundColor White
        }
    }
    
    Write-Host ""
    $confirmar = Read-Host "¿Deseas detener estos procesos? (S/N)"
    
    if ($confirmar -eq "S" -or $confirmar -eq "s") {
        foreach ($proc in $processes) {
            try {
                Stop-Process -Id $proc.Id -Force
                Write-Host "  ✓ Proceso $($proc.ProcessName) detenido" -ForegroundColor Green
            } catch {
                Write-Host "  ✗ Error al detener $($proc.ProcessName)" -ForegroundColor Red
            }
        }
        Write-Host ""
        Write-Host "Puerto 8000 liberado!" -ForegroundColor Green
    } else {
        Write-Host "Operacion cancelada" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "El puerto 8000 esta libre" -ForegroundColor Green
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
