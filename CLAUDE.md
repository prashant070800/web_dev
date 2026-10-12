# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal portfolio for Prashant Singh, served at https://hellops.in (custom domain via `CNAME`, i.e. GitHub Pages). A plain static site with no build step, package manager, framework, linter, or tests: `index.html`, `style.css`, `script.js`, and `images/`.

## Commands

- Preview locally: `python -m http.server 8000`, then open http://localhost:8000
- Build the resume PDF by hand: `powershell -ExecutionPolicy Bypass -File build-resume.ps1`
- One-time setup on a new machine: `winget install MiKTeX.MiKTeX` and `git config core.hooksPath .githooks`

## Resume pipeline

`resume.tex` is the source. `resume.pdf` is a committed build output, and the site links to it from the nav, the sitemap, and elsewhere. `.githooks/pre-commit` runs `build-resume.ps1` whenever `resume.tex` is staged, then stages the new `resume.pdf`. If the LaTeX build fails, the commit is aborted. Edit `resume.tex` and never hand-edit or swap out `resume.pdf`.

`build-resume.ps1` looks for `pdflatex` on PATH, then falls back to MiKTeX's per-user install path. It builds into `.resume-build/` (gitignored) and only replaces `resume.pdf` when the build succeeds.

`.gitattributes` forces LF line endings for `.githooks/*`, because the hook runs under `sh` and CRLF breaks it.

## Page structure and conventions

- `index.html` is one page. Its `<main>` holds the sections `#experience`, `#projects`, `#skills`, `#education` and `#contact`. When you add or rename a section, update the `.nav-link` anchors in the header too. `script.js` highlights the active nav link by matching `href="#id"` against `main section[id]`.
- **Reveal-on-scroll is progressive enhancement:** `script.js` adds a `js` class to `<html>`, and the CSS hides `.reveal` elements only under `.js .reveal` until the IntersectionObserver adds `.visible`. Give new content blocks the `reveal` class if they should animate in.
- **Videos are click-to-load:** a `.video[data-yt="<id>"]` button (with an optional `data-start` in seconds and an `aria-label` of the form "Play …") is swapped for a youtube-nocookie iframe on click.
- **Design tokens** (the dark palette, Inter / JetBrains Mono fonts, radius and container width) live in `:root` at the top of `style.css`. Reuse them rather than adding hard-coded colors.
- **External assets:** Google Fonts, Font Awesome 6 from cdnjs, and GoatCounter analytics, which is loaded at the end of `<body>`.

## SEO metadata kept in sync

Profile facts are duplicated across the `<head>` of `index.html`: the meta description, the Open Graph and Twitter tags, and the JSON-LD `ProfilePage`/`Person` block (job title, employer, `sameAs` links, `knowsAbout`). When the job title, employer, links or tagline change, update all of them together. Bump `<lastmod>` in `sitemap.xml` when the page or the resume changes meaningfully.
