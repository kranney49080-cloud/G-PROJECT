# Installs an ISOLATED Python 3.7.0 (embeddable zip) into tools\py37.
# Nothing is installed system-wide; PATH and registry are untouched.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$dest = Join-Path $root "tools\py37"
$zip  = Join-Path $root "tools\python-3.7.0-embed-amd64.zip"
$url  = "https://www.python.org/ftp/python/3.7.0/python-3.7.0-embed-amd64.zip"

if (Test-Path (Join-Path $dest "python.exe")) {
    Write-Host "Already present: $dest"
} else {
    New-Item -ItemType Directory -Force -Path (Join-Path $root "tools") | Out-Null
    Write-Host "Downloading $url"
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
    Write-Host ("SHA256: " + (Get-FileHash $zip -Algorithm SHA256).Hash)
    Expand-Archive -Path $zip -DestinationPath $dest -Force
}
& (Join-Path $dest "python.exe") -c "import sys, importlib.util; print(sys.version); print('magic', importlib.util.MAGIC_NUMBER)"
