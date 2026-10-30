param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("python-com-cache", "python-sem-cache", "ruby-com-cache", "ruby-sem-cache")]
    [string]$Cenario,

    [Parameter(Mandatory = $true)]
    [int]$Usuarios,

    [int]$SpawnRate = 0,
    [int]$DuracaoSegundos = 90
)

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if ($SpawnRate -le 0) {
    $SpawnRate = [Math]::Min($Usuarios, 10)
}

$hostApi = if ($Cenario -like "ruby*") { "http://api:4567" } else { "http://api:5000" }
$composeFile = Join-Path $Root "compose\$Cenario.yml"
$project = "t4_$Cenario"

& "$PSScriptRoot\set_cenario.ps1" -Cenario $Cenario
Start-Sleep -Seconds 40

$outDir = Join-Path $Root "resultados\$Cenario\users_$Usuarios"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$csvPrefix = "/mnt/locust/resultados/$Cenario/users_$Usuarios/run"

Write-Host "Locust headless: $Cenario | $Usuarios users | ${DuracaoSegundos}s | host=$hostApi"

docker compose -f $composeFile -p $project run --rm `
    -e LOCUST_MODE=api `
    locust `
    -f /mnt/locust/locustfile.py `
    --host=$hostApi `
    --headless `
    -u $Usuarios `
    -r $SpawnRate `
    -t "${DuracaoSegundos}s" `
    --csv $csvPrefix

$statsLocal = Join-Path $outDir "run_stats.csv"
$manifestPath = Join-Path $Root "resultados\manifest.json"
$manifest = @()
if (Test-Path $manifestPath) {
    $manifest = @(Get-Content $manifestPath -Raw | ConvertFrom-Json)
}
$manifest += [ordered]@{
    cenario    = $Cenario
    usuarios   = $Usuarios
    stats_csv  = $statsLocal
    duracao_s  = $DuracaoSegundos
    linguagem  = if ($Cenario -like "python*") { "python" } else { "ruby" }
    cache      = if ($Cenario -like "*-com-cache") { "com" } else { "sem" }
}
($manifest | ConvertTo-Json -Depth 4) | Set-Content -Encoding UTF8 $manifestPath
Write-Host "Stats: $statsLocal"
