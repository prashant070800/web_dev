---
title: Django
category: frameworks
summary: Batteries-included Python web framework.
questions:
  - q: "What happens during a Django request/response cycle?"
    a: |
      The WSGI/ASGI handler builds an `HttpRequest`, request middleware runs, the URL
      resolver picks a view, the view returns an `HttpResponse` (often via templates or
      serializers), and response middleware runs on the way out.
---

## Core concepts

TODO

## How I used it

TODO

## Gotchas

TODO
