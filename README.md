# Prashant Singh — Portfolio

Personal portfolio site, served at [hellops.in](https://hellops.in).

The portfolio is plain static HTML/CSS (`index.html`, `style.css`, `script.js`, `images/`).
The study hub at [hellops.in/study](https://hellops.in/study/) is built by GitHub Pages' Jekyll
from Markdown in `_projects/`, `_experience/`, and `_tech/`.

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

## Adding a study page

Add a Markdown file to `_projects/`, `_experience/`, or `_tech/`. The filename is the slug and the URL
(`_tech/django.md` → `/study/tech/django/`). Front matter:

```yaml
title: Django
summary: One line, shown on the hub card.
category: frameworks        # tech only: languages, frameworks, databases, ai, realtime, cloud
order: 2                    # projects/experience only: position on the hub (lower first)
tech: [django, postgresql]  # projects/experience: tech slugs; links appear automatically
experience: jaxl            # projects only: the role it was built in
company: JAXL               # experience only, with role: and period:
questions:
  - q: "Quote every question"
    a: |
      Markdown answer.
```

Quote any value that contains a colon (`summary: "Backend: APIs"`). Jekyll only warns about broken
front matter, but the site check will fail.

Tech pages list the projects and roles tagged with them automatically. A tag with no page yet
shows as a dashed chip instead of a link.

## Preview the site locally

The portfolio alone can be previewed with `python -m http.server 8000`. To build the study pages too,
start Docker Desktop and run:

```sh
powershell -ExecutionPolicy Bypass -File tools/build-site.ps1 -Serve
```

This builds with the same Jekyll as GitHub Pages, checks the result (`tools/check_site.py`), and serves
`_site/` at http://localhost:8000.
