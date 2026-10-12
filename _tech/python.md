---
title: Python
category: languages
summary: The language behind most of my backend and AI work.
questions:
  - q: "What is the GIL, and when does it matter?"
    a: |
      CPython's Global Interpreter Lock lets only one thread run Python bytecode at a time.
      It limits CPU-bound threading; I/O-bound work still benefits from threads or asyncio,
      and CPU-bound work uses multiprocessing or native extensions.
---

## Core concepts

TODO

## How I used it

TODO

## Gotchas

TODO
