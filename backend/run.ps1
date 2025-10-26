# Carrega as variáveis de ambiente, o ambiente virtual, e executa o programa python

$EnvFile = ".env"
$VenvPath = ".venv\Scripts\Activate.ps1"
$Command = "python main.py"


if (Test-Path $VenvPath) {
    & $VenvPath
}

if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        $_ = $_.Trim()
        if ($_ -and ($_ -notmatch "^\s*#")) {
            if ($_ -match "^\s*([^=]+)\s*=\s*(.*)\s*$") {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim('"').Trim("'")
                [System.Environment]::SetEnvironmentVariable($key, $value)
            }
        }
    }
    Invoke-Expression $Command
} else {
    Write-Host "Arquivo $EnvFile não encontrado!"
}