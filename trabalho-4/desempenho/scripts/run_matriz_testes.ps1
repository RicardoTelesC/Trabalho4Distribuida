# Matriz Trabalho 4: 4 cenarios x 3 niveis de usuarios
# Cada usuario virtual faz 10 GET com URLs distintas.

$UserLevels = @(5, 15, 40)
$Cenarios = @(
    "python-com-cache",
    "python-sem-cache",
    "ruby-com-cache",
    "ruby-sem-cache"
)

foreach ($c in $Cenarios) {
    foreach ($u in $UserLevels) {
        Write-Host "`n=== $c | users=$u ===" -ForegroundColor Cyan
        & "$PSScriptRoot\run_locust_headless.ps1" `
            -Cenario $c `
            -Usuarios $u `
            -DuracaoSegundos 90
    }
}

Write-Host "`nGerando graficos..."
python "$PSScriptRoot\gerar_graficos.py"
