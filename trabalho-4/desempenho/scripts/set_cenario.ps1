param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("python-com-cache", "python-sem-cache", "ruby-com-cache", "ruby-sem-cache")]
    [string]$Cenario
)

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$composeFile = Join-Path $Root "compose\$Cenario.yml"

Write-Host "Parando stacks anteriores..."
Get-ChildItem (Join-Path $Root "compose\*.yml") | ForEach-Object {
    docker compose -f $_.FullName -p "t4_$($_.BaseName)" down 2>$null | Out-Null
}

Write-Host "Subindo cenario: $Cenario"
docker compose -f $composeFile -p "t4_$Cenario" up -d --build

Write-Host "Aguarde ~40s para API/Redis ficarem prontos."
Write-Host "API Python: http://localhost:5000  |  API Ruby: http://localhost:4567  |  Web: http://localhost/"
Write-Host "Locust UI:  http://localhost:8089"
