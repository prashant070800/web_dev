# Prashant Singh — Portfolio

Personal portfolio site, served at [hellops.in](https://hellops.in).

Plain static HTML/CSS: `index.html`, `style.css`, `script.js`, and assets in `images/`.

## Updating the resume

Edit `resume.tex`, then commit. A pre-commit hook rebuilds `resume.pdf` (the file the site links to) automatically.

One-time setup on a new machine:

```sh
winget install MiKTeX.MiKTeX
git config core.hooksPath .githooks
```

### Build the PDF manually

Run from the repo root (works in PowerShell, cmd, or Git Bash):

```sh
powershell -ExecutionPolicy Bypass -File build-resume.ps1
```

This writes `resume.pdf` and cleans up the LaTeX build files. On a LaTeX error it prints the error and leaves the old PDF untouched.

## Preview the site locally

```sh
python -m http.server 8000
```

Then open http://localhost:8000.
