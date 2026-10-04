# Compiles resume.tex -> resume.pdf (the file the site links to) and cleans up build artifacts.
# Usage: powershell -ExecutionPolicy Bypass -File build-resume.ps1
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

$pdflatex = (Get-Command pdflatex -ErrorAction SilentlyContinue).Source
if (-not $pdflatex) {
    $fallback = Join-Path $env:LOCALAPPDATA 'Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
    if (Test-Path $fallback) { $pdflatex = $fallback }
    else { throw 'pdflatex not found. Install MiKTeX: winget install MiKTeX.MiKTeX' }
}

$build = Join-Path $PSScriptRoot '.resume-build'
New-Item -ItemType Directory -Force $build | Out-Null

& $pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$build" resume.tex | Out-Null
if ($LASTEXITCODE -ne 0) {
    Get-Content (Join-Path $build 'resume.log') | Select-String -Pattern '^!' -Context 0, 4 | Out-String | Write-Host
    throw "LaTeX build failed (full log: $build\resume.log)"
}

Copy-Item (Join-Path $build 'resume.pdf') (Join-Path $PSScriptRoot 'resume.pdf') -Force
Remove-Item -Recurse -Force $build
Write-Host 'Built resume.pdf'
