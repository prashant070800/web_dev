# Builds the site exactly like GitHub Pages (github-pages gem in Docker) into _site/, then checks it.
# Usage: powershell -ExecutionPolicy Bypass -File tools/build-site.ps1 [-Serve]
param([switch]$Serve)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot
Set-Location $root

docker run --rm -e PAGES_REPO_NWO=prashant070800/web_dev -v "${root}:/srv/site" -v jekyll-bundle:/usr/local/bundle -w /srv/site ruby:3.3 `
    sh -c "bundle install --quiet && bundle exec jekyll build"
if ($LASTEXITCODE -ne 0) { throw 'Jekyll build failed' }

python tools/check_site.py
if ($LASTEXITCODE -ne 0) { throw 'Site check failed' }

if ($Serve) { python -m http.server 8000 --directory _site }
