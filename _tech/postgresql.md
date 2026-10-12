---
title: PostgreSQL
category: databases
summary: The relational database behind most of my backends.
questions:
  - q: "What causes index bloat, and how do you fix it?"
    a: |
      Under MVCC, every update writes a new row version; updating an indexed column also
      adds index entries, and the dead ones stay until vacuum reclaims them. Fixes: reduce
      update churn on indexed columns (enabling HOT updates), tune autovacuum, and rebuild
      with `REINDEX CONCURRENTLY`.
---

## Core concepts

TODO

## How I used it

TODO

## Gotchas

TODO
