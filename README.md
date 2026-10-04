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

To build manually: `powershell -ExecutionPolicy Bypass -File build-resume.ps1`
