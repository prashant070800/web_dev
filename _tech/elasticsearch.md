---
title: Elasticsearch
category: databases
summary: Distributed full-text search engine.
questions:
  - q: "Why use Elasticsearch instead of SQL LIKE for search?"
    a: |
      Elasticsearch builds an inverted index with analyzers (tokenizing, stemming), so
      full-text queries are fast and ranked by relevance. `LIKE '%term%'` can't use a
      normal B-tree index and has no notion of relevance.
---

## Core concepts

TODO

## How I used it

TODO

## Gotchas

TODO
