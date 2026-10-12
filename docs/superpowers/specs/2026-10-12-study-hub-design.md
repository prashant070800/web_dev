# Study Hub — Design

Date: 2026-10-12 · Status: approved in chat, pending spec review

## Goal

A public interview-prep hub at `hellops.in/study/`. It has one page per project, per role, and per technology, and the pages are cross-linked. You can move from "how the voice bot works" to "Django Channels concepts" to "what I built at QWR" the way an interview jumps between topics. Every page ends with interview questions you can use to quiz yourself.

## Constraints

- **Public content.** Project and experience write-ups explain how things work in general terms. They leave out internal-only details: private endpoints, client names, credentials, and proprietary internals.
- **Hosting.** It stays on GitHub Pages and uses the Jekyll build that Pages already runs, so no CI pipeline is added. The portfolio `index.html` has no front matter, so Jekyll copies it through unchanged.
- **Authoring.** Content is Markdown. Adding a page means adding one `.md` file, and cross-links come from front matter, never from hand-written links.

## Success criteria

1. The hub at `/study/` lists every project, role, and tech page.
2. Every tag reference renders as a working link, or as plain text when the target page doesn't exist yet. No link is broken.
3. Tech and experience pages show their backlinks automatically.
4. The portfolio page renders identically, apart from the new **Study** nav link.
5. Repo-internal files (`CLAUDE.md`, `README.md`, `resume.tex`, `build-resume.ps1`, `docs/`, `.githooks/`) are no longer published.

## Structure

```
_config.yml                 collections, permalinks, exclude list
Gemfile                     github-pages gem (local build matches production)
_layouts/study.html         shell: header/nav, style.css + study.css, GoatCounter
_layouts/study-item.html    detail page (extends study): title, meta, body, questions, related
_includes/related.html      cross-link block
_includes/tag-link.html     one tag → link if a page exists, else plain text
_projects/<slug>.md         → /study/projects/<slug>/
_experience/<slug>.md       → /study/experience/<slug>/
_tech/<slug>.md             → /study/tech/<slug>/
study/index.html            hub (layout: study)
study.css                   study-only styles, using the tokens in style.css
sitemap.xml                 becomes a Liquid template (front matter added)
```

The slug is the filename (`page.slug`), and it is the identifier every tag uses.

## Front matter schema

All three collections share these fields:

```yaml
title: QWR AI Voice Bot
summary: One line, shown on hub cards and in meta description
questions:                    # optional; rendered by the layout, counted on hub
  - q: How did you get time-to-first-audio under 500ms?
    a: |
      Markdown answer.
```

Additional fields per collection:

| Collection   | Extra fields |
|--------------|--------------|
| `projects`   | `experience: <role-slug>` (optional), `tech: [<tech-slug>, …]`, `links: {repo:, demo:}` (optional) |
| `experience` | `company`, `role`, `period` (e.g. `Aug 2024 — Jun 2026`), `tech: [<tech-slug>, …]` |
| `tech`       | `category`: one of `languages`, `frameworks`, `databases`, `ai`, `realtime`, `cloud`, matching the portfolio Skills groups |

## Page body conventions

The body is free Markdown. The skeletons use these headings:

- **Project:** Overview · How it works · Key decisions & trade-offs · Challenges
- **Experience:** Role & team · What I built · Impact
- **Tech:** Core concepts · How I used it · Gotchas

Interview questions are kept out of the body. The layout renders the front matter `questions` as an "Interview questions" section. Each question is a `<details>` element whose `<summary>` is the question and whose content is the answer (run through `markdownify`). This keeps the rendering consistent and lets the hub count the questions.

## Cross-linking rules (`related.html`)

| Page type  | Shows |
|------------|-------|
| Project    | Its tech chips, and its role (if `experience` is set) |
| Experience | Its tech chips, and the projects where `experience == page.slug` |
| Tech       | The projects and roles whose `tech` contains `page.slug` |

`tag-link.html` looks the slug up in the target collection. When the page exists, it renders a link with the page title. When it doesn't, it renders the slug as plain text with a muted style. This is how the design handles missing pages, so authors can tag freely before a tech page exists.

## Hub page (`/study/`)

There are three sections: Projects, Experience, and Tech stack, with Tech grouped by `category` in the portfolio's Skills order. Each card shows the title, the summary, and a question count when it is non-zero. The visual language matches the portfolio: the same tokens, card surfaces, chips, and mono accents.

## Portfolio changes

- `index.html`: add `<a href="study/" class="nav-link">Study</a>` before the Resume button. Because `/study/` isn't a section, the scroll-spy in `script.js` never marks it active, and the link needs no special handling.
- The study layout reuses the portfolio header markup. Its nav links point back to `/#experience` and the other sections, plus Study.

## Config

- `collections`: `projects`, `experience`, `tech`, all with `output: true` and permalinks `/study/<collection>/:name/`.
- `exclude`: `CLAUDE.md`, `README.md`, `resume.tex`, `build-resume.ps1`, `docs/`, `.githooks/`, `Gemfile`, `Gemfile.lock`.
- `.gitignore`: add `_site/`, `.jekyll-cache/`, and `Gemfile.lock`.

## Starter content (skeletons, bodies are TODO)

- **Projects:** `qwr-voice-bot`, `vargi-bot`, `construct-o-bot`
- **Experience:** `qwr`, `jaxl`, `infosys`, `jaxl-intern`
- **Tech:** `python`, `django`, `django-rest-framework`, `django-channels`, `flask`, `flutter`, `postgresql`, `elasticsearch`, `redis`, `websockets`, `gemini-live-api`, `rag`, `gcp`

Front matter (titles, summaries, periods, tech tags) comes from the existing portfolio content. Each body has the section headings with a TODO line. Each page gets one example question so the rendering can be checked.

## Verification

1. Build with Docker so the local result matches production: `docker run --rm -v "$PWD":/srv -w /srv ruby:3.3 sh -c "bundle install && bundle exec jekyll build"`.
2. Check that `_site/study/**` contains every expected page, and that `_site/index.html` is byte-identical to the source `index.html`, which proves Jekyll passed it through untouched.
3. Scan the generated HTML so that every internal `href` resolves to a file in `_site/`.
4. Check that the excluded files are absent from `_site/`.
5. Visually check the pages by serving `_site/` with `python -m http.server`.

## Docs

Update `CLAUDE.md` and `README.md`: how to add a study page, the front matter schema, how tags link, and the Docker build or preview command.

## Out of scope

Search, dark/light theme toggle, comments, private content, a separate subdomain.
