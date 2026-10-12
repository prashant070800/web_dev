---
title: Django Channels
category: frameworks
summary: Long-lived connections (WebSockets) in Django over ASGI.
questions:
  - q: "How is a Channels consumer different from a Django view?"
    a: |
      A view handles one HTTP request and returns one response. A consumer runs under
      ASGI and handles a long-lived connection as events: `connect`, `receive`, and
      `disconnect`. A channel layer (usually Redis) lets consumers in different
      processes message each other, for example to broadcast to a group.
---

## Core concepts

TODO: ASGI, consumers (sync vs async), routing, channel layers and groups.

## How I used it

TODO: streaming call audio for the voice bot.

## Gotchas

TODO: blocking calls inside async consumers, database access from async code, scaling the channel layer.
